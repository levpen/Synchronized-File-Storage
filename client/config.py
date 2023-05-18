import json
import os


CONFIG_FILE = os.path.dirname(os.path.abspath(__file__)) + '/config.json'


class Config:
    def __init__(self, addr=None):
        self.addr = addr

    def setup(self):
        words = [
            '1) Server addr: ',
        ]
        self.addr = input(words[0])

        if len(self.addr) > 0 and self.addr[-1] == '/':
            self.addr = self.addr[:-1]

    def save_file(self):
        with open(CONFIG_FILE, 'w') as file:
            file.write(str(self))
        print('Saved ✔✔✔')

    def __str__(self):
        m = {
            'addr': self.addr,
        }
        return json.dumps(m)


def read_config():
    try:
        with open(CONFIG_FILE, 'r') as file:
            data = json.loads(file.read())
            conf = Config(addr=data['addr'])
            return conf
    except Exception as err:
        print(f"ERROR: while reading config: {err}\n❗️❗️❗  Run setup command or create config.json")
        return None
