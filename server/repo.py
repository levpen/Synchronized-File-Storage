import time
import os
import pickle


class Repo:
    def __init__(self):
        self.history = {}
        with open('../.history', 'rb') as f:  # deserializing dict with history of changes
            self.history = pickle.load(f)
        pass

    def __del__(self):
        with open('../.history', 'wb') as f:  # serializing dict with history of changes
            pickle.dump(self.history, f)

    def save(self, filename, data):  # saves file with given name
        self.history[filename] = int(time.time())
        if '/' in filename:
            os.mkdir(f'../storage/{filename[:filename.rfind("/")]}')
        with open(f'../storage/{filename}', 'wb') as f:
            f.write(data)

    def get_since(self, date: int, directory):  # returns names of files since date
        files = []
        for name, time in self.history.items():
            if time >= date:
                if directory == '' or name.startswith(directory):
                    files.append(name)
        return files

    def get(self, filename):  # returns file in binary format with given name
        if filename not in self.history.keys():
            raise FileNotFoundError
        with open('../storage/' + filename, 'rb') as f:
            data = f.read()
            return data

    def delete(self, filename):
        del self.history[filename]
        os.remove('../storage/' + filename)
