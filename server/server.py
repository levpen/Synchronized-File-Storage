from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:

            path = self.path.split('?')[0]
            args = {}
            if self.path.find('?') != -1:
                for p in self.path.split('?')[1].split('&'):
                    args[p.split('=')[0]] = p.split('=')[1]

            if path == '/get_since':
                if 'date' not in args.keys():
                    self.send_response(418)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b'The server responded with a status of 418 (I\'m a Teapot)</br> Parameter date '
                                     b'should be defined')
                    return
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Hello, world! since + ' + args['date'].encode())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Not found')
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'Internal Server Error')

    def do_POST(self):
        self.send_response(501)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response = BytesIO()
        response.write(b'Not implemented')
        self.wfile.write(response.getvalue())


try:
    httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
    httpd.serve_forever()
except KeyboardInterrupt:
    httpd.shutdown()
