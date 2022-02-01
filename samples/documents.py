import os
from config import BASE_URL
from samples import helpers
from typing import Dict, List, Union


def fetch_and_send_document():
    """
    Fetch your XML documents and send them to CoAPI.
    You can set up your ftp server to retrieve your documents, however,
    we are getting our document from the sbds folder here.
    
    In order to successfully send a document,
    you must be sure that it follows the guidelines provided by Sovos
    For more information: [developer guide](https://developer-guide.sovos.com/connect-once-api/general-concepts/standard-business-document)
    """
    filepath = os.path.abspath("sbds/document.xml")
    with open(filepath, mode="r", encoding="utf8") as f:
        doc = f.read()

    # modify XML if necessary
    # ...

    # send the document to CoAPI
    return send_document(doc)
    

def execute_document_action(
        country_code: str,
        action_code: helpers.DocumentActionCodes,
        documents: List[Dict[str, Union[str, Dict[str, str]]]]
    ):
    """
    This method shows how the request should look when you want to cancel a document.
    Please pay attention to Correlation Id and Idempotency Key headers.
    
    For more information, please visit:
    [documentation](https://developer.sovos.com/apis/e-invoicing#operation/Document_PostActionMultipleDocs) or\
    [developer guide](https://developer-guide.sovos.com/connect-once-api/general-concepts/api-specifications/sending-and-retrieving-documents)

    :param str country_code: The two-digit country code specified by the ISO 3166-1 alpha-2 standard
    """

    url = f"{BASE_URL}/v1/documents/{country_code}/action"
    payload = {
        'actionCode': action_code.value,
        'documents': documents
    }
    
    headers = helpers.generate_headers()
    response = helpers.requests_retry_session().request(
        "POST", url, headers=headers, json=payload)
    
    # TODO: handle cancel document response
    print(response.status_code)

    return response.json()


def send_document(document: str):
    """
    This method shows how the request should look when you want to send a document.
    Please pay attention to Correlation Id and Idempotency Key headers.

    For more information, please visit:
    [documentation](https://developer.sovos.com/apis/e-invoicing#operation/Document_Post) or\
    [developer guide](https://developer-guide.sovos.com/connect-once-api/general-concepts/api-specifications/sending-and-retrieving-documents)
    
    @param {string} document stringified Sovos Business Document
    """
    url = f"{BASE_URL}/v1/documents"
    data = helpers.tobase64(document).decode()

    payload = {"data": data, "dataEncoding": "base64"}

    headers = helpers.generate_headers(
        isPostRequest=True,
        payload=payload
    )
    response = helpers.requests_retry_session().request(
        "POST", url, headers=headers, json=payload)
    
    # TODO: handle document response
    print(response.status_code)

    return response.json()

