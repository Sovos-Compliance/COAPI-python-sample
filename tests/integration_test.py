from samples import notifications
from samples import documents
from samples import helpers
from samples.auth import auth
import config
import time


def test_access_token():
  token = auth.get_access_token()
  issued_at = auth._last_response.get("issued_at")
  assert 0 < len(token)
  assert "approved" == auth._last_response.get("status")

  time.sleep(2)
  second_token = auth.get_access_token()
  second_issued_at = auth._last_response.get("issued_at")
  assert token == second_token
  assert issued_at == second_issued_at


  now = int(time.time())
  auth.set_access_token_expire(now)
  third_token = auth.get_access_token()
  assert 0 < len(third_token)
  assert "approved" == auth._last_response.get("status")
  assert third_token != second_token and third_token != token
  assert issued_at != auth._last_response.get("issued_at")


def test_send_document():
  response = documents.fetch_and_send_document()
  assert 202 == response.get("status")
  assert 'Document Received' == response.get("message")
  

def test_get_notifications_by_search_criteria():
  response = notifications.get_notifications(
    country_code=config.COUNTRY_CODE,
    taxId=config.SENDER_TAX_ID,
    sourceSystemId=config.SENDER_SYSTEM_ID,
    page=1,
    perPage=1,
    includeAcknowledged="true"
  )
  assert 200 == response.get("status")
  assert 'Notifications Listed' == response.get("message")


def test_mark_notification():
  get_notification_request = notifications.get_notifications(
    country_code=config.COUNTRY_CODE,
    taxId=config.SENDER_TAX_ID,
    sourceSystemId=config.SENDER_SYSTEM_ID,
    page=1,
    perPage=1,
    includeAcknowledged="true"
  )
  assert 200 == get_notification_request.get("status")
  notification_id = get_notification_request.get("data").get("notifications")[0].get("notificationId")

  response = notifications.mark_notifications(
    country_code=config.COUNTRY_CODE, 
    notification_ids=[notification_id],
    status="read"
  )
  assert 200 == response.get("status")
  assert 'Notifications acknowledged successfully.' == response.get("message")


def test_cancel_document():
  document_id = config.SAMPLE_DOCUMENT_ID
  document_item = helpers.generate_action_document_item(
    document_id=document_id,
    reason="Reason for cancelling the document"
  )
  response = documents.execute_document_action(
    country_code=config.COUNTRY_CODE,
    action_code=helpers.DocumentActionCodes.CANCELLATION,
    documents=[document_item]
  )
  assert 202 == response.get("status")
  assert 'Action Received' == response.get("message")
  assert document_id == response["data"][0]["documentId"]

