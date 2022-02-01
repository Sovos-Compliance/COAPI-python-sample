# Sovos CoAPI Python Code Sample

This repository contains a sample implementation for the client to make the following requests:
- Generate access token
- Send an invoice document
- Take actions such as cancelling, correction or distribution of a created document
- Retrieve notifications
- Acknowledge notifications

## Setup
Download [Python](https://www.python.org/downloads)

Install dependencies:
```
pip install -r requirements.txt
```

The code sample makes use of **[dotenv package][dep]**. This is why the environment variables are configured in an .env file in the root folder.

Set up your .env file accordingly.

| Variable | Description |
| -------- | ----------- |
| BASE_URL | https://api.sovos.com * |
| API_KEY | API key that you receive when you create your app on the [developer portal][devportal]. |
| SECRET_KEY | API Secret key that you receive when you create your app on the [developer portal][devportal]. |
| SENDER_TAX_ID | Your tax ID |
| SENDER_SYSTEM_ID | System ID provided by Sovos |
| RETRY_LIMIT | You may want to limit the resending requests in case they fail for your convenience. |
| COUNTRY_CODE | The country code that you are using the APIs for |
| SAMPLE_DOCUMENT_ID | You may need to provide a document ID for one of the test case scenarios |


*There are three BASE URLs for different use cases:

| Production | Sandbox | TLS |
| ---------- | ------- | --- |
| https://api.sovos.com | https://api-test.sovos.com | https://api-test-tls.sovos.com |

Please visit [the developer guide][dgapispecs] for more information on Base URLs & API Specifications.

Before you can move on to run anything, please check out the basic examples in the **main.py** file. For sending documents, you must have created a SBD ([Standard Business Document][sbd]) yourself. Then, you can send this document to CoAPI by following either of these steps:
1. Use `fetch_and_send_document` method as shown as an example in the main.py:
    1. Name your SBD file as "document.xml",
    2. Move it into the **sbds** folder.
2. Use document service:
    1. Run your document service with by uncommenting the relevant lines in main.py.
    2. Send a POST request with your document in Base64 format to this server with below configuration:
        - Route: /send-document
        - Sample Payload (in JSON): { "data": "PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz..." }

Please check out the implementation for both `fetch_and_send_document` method and the document service, and make changes if necessary.

If you have completed the steps above, then run:
```
python main.py
```

## Testing
```
pytest -v
```
If you have configured your environment variables correctly, and followed the steps above to configure how you send documents to CoAPI, you should now be able to run tests and see the outcomes for yourself. You can follow the logic in the tests to make your own request in your own environment.


## Understanding the Code Sample
Connect Once API requires an **access token** to be provided in the Authentication header. In order to get an access token, you must use Basic Authentication with the provided API key and API secret key. Please visit the [developer guide][dgauth] for more information. This generated access token will expire in 1 hour, after which you must generate a new access token. Cache and reuse the token for the duration of its validity instead of continuously generating new token.

You are also required to have **x-correlationId** header for all requests as specified in the [documentation][dgapispecs], and you will need to have an **X-Idempotency-Key** header for the POST requests as specified in the [documentation][dgidemreq].

You can send documents or cancel them. After the documents are approved, you can send a cancellation request with the provided samples.

You will have notifications for the documents, and you should acknowledge them. You can view and acknowledge the notifications as shown in the provided code samples.

### Further Configuration
We are handling requests via requests package as seen in the function `requests_retry_session` in **samples/helpers.py** file. You can change your configuration here. Please checkout the file and the [developer guide][dgerrhandling] to read about responses in more detail.

**IMPORTANT!**
We urge you to you update how you handle responses & errors in your requests. The parts that require your own implementations are marked as todos (as TODO:), which you should be able to easily see in your IDE.

### Methods
samples/documents.py will help you
- send a document
- take an action on documents: cancel, correct or distribute documents.

Please do not forget that you may have to wait for while before the document is approved. Only then you will be able to see the notifications or take an action on the documents. Otherwise, if the document isn't confirmed to be approved, you might risk attempting to cancel a rejected document.

samples/notifications.py will help you
- retrieve documents
- acknowledge documents, or mark documents as unread.

You can follow the implementations in  **main.py** file or in the test file to see how we make requests to Once Connect API.


[sbd]: <https://developer-guide.sovos.com/connect-once-api/general-concepts/standard-business-document>
[dep]: <https://pypi.org/project/python-dotenv/>
[dgapispecs]: <[https://developer-guide.sovos.com/connect-once-api/general-concepts/api-specifications]>
[dgauth]: <https://developer-guide.sovos.com/connect-once-api/general-concepts/api-specifications/authentication>
[dgerrhandling]: <https://developer-guide.sovos.com/connect-once-api/general-concepts/responses>
[devportal]: <https://developer.sovos.com>
[dgidemreq]: <https://developer-guide.sovos.com/connect-once-api/general-concepts/idempotent-requests/>