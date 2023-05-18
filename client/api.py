import os
import urllib.request
import urllib.response
import urllib.error

from config import Config

SYNC_ENDPOINT = "/get_since"
PUSH_ENDPOINT = "/post"
PING_ENDPOINT = "/ping"
DELETE_ENDPOINT = "/delete"


class ApiClient:

    def __init__(self, conf):
        self.conf: Config = conf

    def ping(self) -> bool:
        dst_url = f"{self.conf.addr}{PING_ENDPOINT}"
        try:
            urllib.request.urlopen(dst_url)
            return True
        except Exception as err:
            print(f"ERROR: failed to ping server: {err}")
            return False

    def sync(self, date_from, dirs):
        date_from = int(date_from)
        dst_url = f"{self.conf.addr}{SYNC_ENDPOINT}?date={date_from}"
        if dirs:
            dst_url += f"&dir={','.join(dirs)}"
        try:
            req = urllib.request.Request(dst_url, method='GET')
            resp = urllib.request.urlopen(req)
            data = resp.read()
            return data
        except urllib.error.HTTPError as e:
            print(f"INFO\thttp error for file: error={e}")
            return False
        except urllib.error.URLError as e:
            print(f"ERROR\terror while pulling file error={e}")
            return False
        except Exception as e:
            print(f"ERROR\t unknown error={e}")

    def push(self, file_name) -> bool:
        dst_url = f"{self.conf.addr}{PUSH_ENDPOINT}?name={file_name}"
        try:
            file_bytes = open(file_name, 'rb').read()
            try:
                file_bytes.decode('utf-8')
            except Exception as e:
                print(f"ERROR\tcould not decode file: {file_name}, error={e}\n❗️❗️❗️ Note: only utf-8 files")
                return False
            req = urllib.request.Request(dst_url, file_bytes, method='POST')
            req.add_header('Content-Length', str(os.stat(file_name).st_size))
            urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            print(f"INFO\thttp error for file: {file_name}, error={e}")
            return False
        except urllib.error.URLError as e:
            print(f"ERROR\terror while deleting file {file_name}, error={e}")
            return False
        except Exception as e:
            print(f"ERROR\t unknown error for file {file_name}, error={e}")
        else:
            return True

    def delete(self, file_name):
        dst_url = f"{self.conf.addr}{DELETE_ENDPOINT}?name={file_name}"
        try:
            req = urllib.request.Request(dst_url, method='DELETE')
            urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                print(f"INFO\tno such file on server: {file_name}")
                return False
            print(f"ERROR\terror while deleting file {file_name}, status_code={e.code}")
            return False
        except urllib.error.URLError as e:
            print(f"ERROR\terror while deleting file {file_name}, error={e}")
        else:
            return True
