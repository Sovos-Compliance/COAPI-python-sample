import base64
import hashlib
import logging
import requests
import requests.adapters
import urllib3
import uuid
from enum import Enum
from samples.auth import auth
from typing import Dict
import config


logging.basicConfig(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.DEBUG)


class DocumentActionCodes(Enum):
    CANCELLATION = "document.cancellation"
    CORRECTION = "document.correction"
    DISTRIBUTE = "document.distribute"

status_forcelist = [408, 429] + [x for x in range(500, 600) if x != 501]
def requests_retry_session(
    retries=config.RETRY_LIMIT,
    backoff_factor=0,
    status_forcelist=status_forcelist,
    session=None,
):
    session = session or requests.Session()
    retry = urllib3.Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        raise_on_status=False,
        respect_retry_after_header=True
    )
    adapter = requests.adapters.HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def generate_headers(
        isPostRequest:bool=False,
        payload: Dict[str, str]={}
    ) -> Dict[str, str]:
    """
    Generate headers for the requests.
    You must provide payload if you are generating headers for a POST request.
    """

    token = auth.get_access_token()
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer " + token,
        "x-correlationId": generate_correlation_id(),
    }
    if isPostRequest:
        headers["X-Idempotency-Key"] = generate_idempotency_key(payload)

    return headers


def generate_action_document_item(document_id: str, **kwargs):
    """
    Args:
        documentId str: Document ID
        **kwargs: Metadata for the document dictionary. Some parameters are required.
    
    Keyword Args:
        reason str: required
        reasonCode str or null: optional
        companyId str or null: optional
        branchId str or null: optional
        documentType str or null: optional
        documentReferenceID str or null: optional
    """
    return { "documentId": document_id, "metadata": kwargs }


def tobase64(string): 
    s = str(string)
    base64_string = base64.b64encode(s.encode("utf8"))
    return base64_string


# TODO: Write your own implemantation if necessary
def generate_correlation_id():
    """
    "x-correlationId" must be set to a universally unique identifier (UUID).
    This value can be used to track transactions for debugging purposes.
    
    This is not the only correct way to generate a correlation id.
    You have to make your own implementation.
    """
    return str(uuid.uuid4())


# TODO: Write your own implemantation if necessary
def generate_idempotency_key(payload):
    """
    An idempotency key is a unique value generated by the client which
    the server uses to recognize subsequent retries of the same request.
    
    This is not the only correct way to generate an idempotency key.
    You have to make your own implementation.
    
    For more information, please visit: \
    [developer guide](https://developer-guide.sovos.com/connect-once-api/general-concepts/idempotent-requests)
    """
    return hashlib.md5(str(payload).encode()).hexdigest()
