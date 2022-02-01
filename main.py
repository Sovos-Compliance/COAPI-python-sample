import base64
import config
import json
import samples.documents as documents
import samples.helpers as helpers
import samples.notifications as notifications
from services.document import start_document_service


def main():
    # You should have a service where you create your own
    # SBD (Standard Business Document), and where you can fetch
    # your SBD files from. In this example, we are getting
    # our document from the sbds folder in this project.
    # You will either add a SBD file in the sbds folder, or change
    # the implementation of the below method.
    # 
    # For more information on SBD:
    # https://developer-guide.sovos.com/connect-once-api/general-concepts/standard-business-document
    new_doc_response = documents.fetch_and_send_document()

    print(
        "[DOCUMENT CREATED]\n",
        json.dumps(new_doc_response, indent=4, sort_keys=True)
    )


    # You can retrieve all notifications.
    # Please pay attention to limits:
    # page parameter's range is [1, 10]
    # perPage parameter's range is [1, 100] if includeBinaryData is false, and
    # perPage parameter's range is [1, 10] if includeBinaryData is true.
    notifications_response = notifications.get_notifications(
        country_code=config.COUNTRY_CODE,
        taxId=config.SENDER_TAX_ID,
        sourceSystemId=config.SENDER_SYSTEM_ID,
        page=1,
        perPage=1,
        includeAcknowledged="true"
    )

    print(
        "\n",
        "[NOTIFICATIONS]\n",
        json.dumps(notifications_response, indent=4, sort_keys=True)
    )

    # you can check the notification content:
    # sample_notification = notificationsResponse["data"]["notifications"][0]["content"]
    # content = base64.b64decode(sample_notification)
    # print(content)

    # if you have no notifications, the status code will be 404.
    if notifications_response['status'] == 200:
        # You can also get a single notification by id
        # or a single notification by id
        notification_id = notifications_response.get("data").get("notifications")[0].get("notificationId")
        notification_by_id_response = notifications.get_notification_by_id(
            country_code=config.COUNTRY_CODE,
            notification_id=notification_id
        )
        print(
            "\n",
            "[NOTIFICATION BY ID]\n",
            json.dumps(notification_by_id_response, indent=4, sort_keys=True)
        )

        notif_doc_id = notifications_response.get("data").get("notifications")[0].get("metadata").get("documentId")
        notifications_by_document_id = notifications.get_notification_by_document_id(
        config.COUNTRY_CODE, document_id=notif_doc_id, includeAcknowledged="false")
        print(
            "\n",
            "[NOTIFICATION BY DOCUMENT ID]:\n",
            json.dumps(notifications_by_document_id, indent=4, sort_keys=True)
        )


        # You can acknowledge notificitations
        notification_list = notifications_response["data"]["notifications"]
        notification_ids = [item["notificationId"] for item in notification_list]
        mrk_ntf_resp = notifications.mark_notifications(
            country_code=config.COUNTRY_CODE, 
            notification_ids=notification_ids,
            status="read"
        )

        print(
            "\n",
            "[NOTIFICATIONS ACKNOWLEDGED]:\n",
            json.dumps(mrk_ntf_resp, indent=4, sort_keys=True)
        )

    # or you may want to mark these notifications as "unread" if you think
    # they are not processed properly
    # notifications_unread = notifications.mark_notifications(
    #     country_code=config.COUNTRY_CODE, 
    #     notification_ids=notification_ids,
    #     status="unread"
    # )
    # print(
    #     "\n",
    #     "[NOTIFICATIONS UNREAD]:\n",
    #     json.dumps(notifications_unread, indent=4, sort_keys=True)
    # )

    # Actions on documents: you may cancel, correct or distribute documents.
    # Here, documentId represents a document that was created and approved
    # prior to this call. You will not be able to cancel the document
    # before it is approved.
    # 
    # Set an approved document id for the SAMPLE_DOCUMENT_ID if you want to
    # use the code below
    doc_id = config.SAMPLE_DOCUMENT_ID
    if doc_id:
        doc_item = helpers.generate_action_document_item(
            document_id=doc_id,
            reason="Reason for cancelling the document"
        )
        doc_act_resp = documents.execute_document_action(
            country_code=config.COUNTRY_CODE,
            action_code=helpers.DocumentActionCodes.CANCELLATION,
            documents=[doc_item]
        )
        print(
            "\n",
            "[DOCUMENT CANCELLATION]:\n",
            json.dumps(doc_act_resp, indent=4, sort_keys=True)
        )


main()

# start document service in port 3000 if you like
# start_document_service()