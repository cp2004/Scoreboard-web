import os, json


class DataManager():
    def __init__(self, app):
        self.basedir = os.path.dirname(__file__)
        self.DATA_DIR = os.path.join(self.basedir, app.config['DATA_DIRECTORY'])

        if not os.path.isdir(self.DATA_DIR):
            os.mkdir(self.DATA_DIR)

    def readFile(self, name, dir=None):
        try:
            with open(self.getPath(name, dir), 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            # LOG EVENT: FILE NOT FOUND
            return None

    def writeFile(self, name, data, dir=None):
        if dir:
            if not os.path.isdir(os.path.join(self.DATA_DIR, dir)):
                os.makedirs(os.path.join(self.DATA_DIR, dir))

        with open(self.getPath(name, dir), 'w') as file:
            json.dump(data, file)

    def deleteFile(self, name, dir=None):
        path = self.getPath(name, dir)
        if self.file_exists(name, dir='games'):
            os.remove(path)
        else:
            print("File not found")

    def file_exists(self, name, dir=None):
        return os.path.isfile(self.getPath(name, dir))

    def getPath(self, name, dir=None):
        if dir:
            return os.path.join(self.DATA_DIR, dir, '{}.json'.format(name))
        else:
            return os.path.join(self.DATA_DIR, '{}.json'.format(name))
