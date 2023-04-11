import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from repository import all, retrieve, create, update, delete
from urllib.parse import urlparse

class HandleRequests(BaseHTTPRequestHandler):
   
    def do_GET(self):
        response = None
        (resource, id, query_params) = self.parse_url(self.path)
        if id is not None:
            self._set_headers(200)

            response = retrieve(resource, id, query_params)
        else:
            self._set_headers(200)
            response = all(resource)

        self.wfile.write(json.dumps(response).encode())
    

    # Replace existing function with this
    def parse_url(self, path):
        url_components = urlparse(path)
        path_params = url_components.path.strip("/").split("/")
        query_params = url_components.query.split("&")
        resource = path_params[0]
        id = None

        try:
            id = int(path_params[1])
        except IndexError:
            pass
        except ValueError:
            pass

        return (resource, id, query_params)

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        "Test"
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (type, id, query_params) = self.parse_url(self.path)

        if type == "orders":
            self._set_headers(201)
            new_resource = create(type, post_body)
            self.wfile.write(json.dumps(new_resource).encode())
        else:
            self._set_headers(405)
            self.wfile.write(f"You cannot create new {type}".encode())

    # A method that handles any PUT request.
    def do_PUT(self):
        "Test"
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (type, id, query_params) = self.parse_url(self.path)

        if type == "metals":
            self._set_headers(204)
            update(id, type, post_body)
            self.wfile.write("".encode())
        else:
            self._set_headers(405)
            self.wfile.write(f"You cannot change {type}".encode())

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_DELETE(self):
        "Test"
        # Set a 405 response code
        self._set_headers(405)

        # Parse the URL
        (type, id, query_params) = self.parse_url(self.path)

        self.wfile.write(f"You cannot delete {type}".encode())

# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
