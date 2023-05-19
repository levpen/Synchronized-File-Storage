import json
import socketserver
import repo
import serverbase
from http.server import HTTPServer


class SimpleHTTPRequestHandler(serverbase.ServerBase):
    def __init__(self, request: bytes, client_address: tuple[str, int], server: socketserver.BaseServer):
        self.repo = repo.Repo()
        super().__init__(request, client_address, server)

    def get_get_since(self, path, args):
        if 'date' not in args.keys():
            self._arg_not_found()
            return
        directory = ''
        if 'dir' in args.keys():
            directory = args['dir']
        data = {}
        files = self.repo.get_since(int(args['date']), directory)
        for file in files:
            data[file] = self.repo.get(file).decode()
        self._standard_resp(json.dumps(data).encode())

    def get_ping(self, path, args):
        self._standard_resp(b'')

    def post_post(self, path, args):
        data = self.rfile.read(int(self.headers['Content-Length']))
        name = args['name']
        self.repo.save(name, data)

        self._standard_resp(b'ok')

    def delete_delete(self, path, args):
        name = args['name']
        if not self.repo.exists(name):
            self._standard_resp(b'file doesnt exist')
        self.repo.delete(name)
        self._standard_resp(b'ok')

HOST = '0.0.0.0'
PORT = 8000

try:
    httpd = HTTPServer((HOST, PORT), SimpleHTTPRequestHandler)
    print('fileserver has started!', HOST, PORT)
    httpd.serve_forever()
except KeyboardInterrupt:
    httpd.shutdown()
