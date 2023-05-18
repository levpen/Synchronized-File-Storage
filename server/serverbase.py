from http.server import BaseHTTPRequestHandler


class ServerBase(BaseHTTPRequestHandler):
    def _arg_not_found(self):
        self.send_response(418)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'The server responded with a status of 418 (I\'m a Teapot)</br> Parameter date '
                         b'should be defined')

    def _standard_resp(self, data):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(data)

    def _not_found_resp(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Not found')

    def _internal_error_resp(self):
        self.send_response(500)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Internal Server Error')

    def _handle(self):
        print(f'{self.command} req on {self.path}')
        try:
            path = self.path.split('?')[0]
            args = {}
            if self.path.find('?') != -1:
                for p in self.path.split('?')[1].split('&'):
                    args[p.split('=')[0]] = p.split('=')[1]
            try:
                getattr(self, self.command.lower() + '_' + path[1:].replace('/', '_'))(path, args)
            except Exception as e:
                print(e)
                self._not_found_resp()
        except Exception as e:
            print(e)
            self._internal_error_resp()

    def do_GET(self):
        self._handle()

    def do_POST(self):
        self._handle()

    def do_DELETE(self):
        self._handle()
