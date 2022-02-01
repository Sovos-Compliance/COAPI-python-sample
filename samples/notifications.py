from config import BASE_URL
from samples import helpers
from typing import List


def get_notifications(country_code, **params):
    """
    Get notifications.

    For more information, please visit: [documentation](https://developer.sovos.com/apis/e-invoicing#operation/Notifications_Get) or \
    [developer guide](https://developer-guide.sovos.com/connect-once-api/general-concepts/api-specifications/retrieving-and-acknowledging-notifications)

    Args:
        country_code str: The two-digit country code specified by the ISO 3166-1 alpha-2 standard
        **params: Parameters for the notifications request. Some parameters are required.
    
    Keyword Args:
        taxId str: Sender tax ID | required
        sourceSystemId str: Sender System ID | required
        page int: The page of results to return. The default is 1
        perPage int: Specifies how many results to return for this page. The Default is 50
        includeAcknowledged str: Determines whether previously acknowledged notifications will be included in the response or not. 
        The default behavior is "false".
        includeBinaryData str: Determines whether binary data will be included in the application response instead of only URLs. 
        The default behavior is "false".
        processType int: Determines whether outbound or inbound notifications will be retrieved.
        Use "0" for outbound and "1" for inbound. 
        Excluding this will lead to the inclusion of both outbound and inbound notifications.
    """

    url = f"{BASE_URL}/v1/notifications/{country_code}"    
    headers = helpers.generate_headers()
    response = helpers.requests_retry_session().request(
        "GET", url, headers=headers, params=params)
    
    # TODO: handle notifications response
    print(response.status_code)

    return response.json()


def get_notification_by_id(country_code: str, notification_id: str, includeBinaryData=False):
    """
    Get a notification by its id.

    For more information, please visit: [documentation](https://developer.sovos.com/apis/e-invoicing#operation/Document_GetNotifications) or \
    [developer guide](https://developer-guide.sovos.com/connect-once-api/general-concepts/api-specifications/retrieving-and-acknowledging-notifications)

    :param str country_code: The two-digit country code specified by the ISO 3166-1 alpha-2 standard
    :param str notification_id: Notification ID
    :param bool includeBinaryData: Determines whether binary data will be included in the application
    response instead of only URLs. The default behavior is "false".
    """
    url = f"{BASE_URL}/v1/notifications/{country_code}/{notification_id}"   
    headers = helpers.generate_headers()
    params = {"includeBinaryData": includeBinaryData}
    response = helpers.requests_retry_session().request(
        "GET", url, headers=headers, params=params)
    
    # TODO: handle notifications response
    print(response.status_code)
    return response.json()


def get_notification_by_document_id(
        country_code: str,
        document_id: str,
        includeAcknowledged="false",
        includeBinaryData="false"
    ):
    """
    Get notifications related to a document.

    For more information, please visit: [documentation](https://developer.sovos.com/apis/e-invoicing#operation/Document_GetNotifications) or\
    [developer guide](https://developer-guide.sovos.com/connect-once-api/general-concepts/api-specifications/retrieving-and-acknowledging-notifications)

    :param str country_code: The two-digit country code specified by the ISO 3166-1 alpha-2 standard
    :param str document_id: Document ID
    :param str includeAcknowledged: Determines whether binary data will be included in the application.
    The default behavior is "false".
    :param str includeBinaryData: Determines whether binary data will be included in the application
    response instead of only URLs. The default behavior is "false".
    """
    url = f"{BASE_URL}/v1/documents/{country_code}/{document_id}/notifications"   
    headers = helpers.generate_headers()
    params = {
        "includeAcknowledged": includeAcknowledged,
        "includeBinaryData": includeBinaryData
    }
    response = helpers.requests_retry_session().request(
        "GET", url, headers=headers, params=params)
    
    # TODO: handle notifications response
    print(response.status_code)
    return response.json()


def mark_notifications(country_code: str, notification_ids: List[str], status="read"):
    """
    You can mark processed notifications as "read",
    or mark notifications that have not been properly processed as "unread"
    For more information, please visit: [documentation](https://developer.sovos.com/apis/e-invoicing#operation/Notifications_Put) or \
    [developer guide](https://developer-guide.sovos.com/connect-once-api/general-concepts/api-specifications/retrieving-and-acknowledging-notifications)

    :param str country_code: The two-digit country code specified by the ISO 3166-1 alpha-2 standard
    :param iterable notification_ids: List of notification ids
    :param str status: Status of the notifications to be marked. This could be either "read" or "unread"
    """

    url = f"{BASE_URL}/v1/notifications/{country_code}"
    payload = [{"status": status, "notificationId": id} for id in notification_ids]
    headers = helpers.generate_headers()
    response = helpers.requests_retry_session().request(
        "PUT", url, headers=headers, json=payload)

    # TODO: handle marked notifications response
    print(response.status_code)

    return response.json()