import base64
import json
from samples import documents
from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus


# TODO: Update how you handle your document service
class HandleRequests(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self.send_error(HTTPStatus.NOT_IMPLEMENTED)


    # You can configure how your service will accept the data, but
    # in our case, we are expecting a base64 encoded string for the data,
    # so we are decoding the data, making the necessary changes, and
    # sending it to the CoAPI.
    def do_POST(self):
        if self.path != '/send-document':    
            self.send_error(HTTPStatus.NOT_IMPLEMENTED)
            return
        
        content_len = int(self.headers.get('Content-Length', 0))
        try:
            post_body = json.loads(self.rfile.read(content_len))
            doc = base64.b64decode(post_body["data"]).decode()

            # modify XML document if necessary
            # ...

            # our document.send method requires an xml string,
            # and will do the necessary base64 conversion before making the request
            response = documents.send_document(doc)
            
            self._set_headers()
            self.wfile.write(bytes(json.dumps(response), "utf-8"))


        except:
            self.send_error(HTTPStatus.BAD_REQUEST)


def start_document_service():
    HTTPServer(('', 3000), HandleRequests).serve_forever()
