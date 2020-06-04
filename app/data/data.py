import os
import json


class DataManager():
    """Manage reading and writing data
    """
    def __init__(self, app):
        """Initialise the manager

        Args:
            app (Flask): App instance so config is accessible
        """
        self.basedir = os.path.dirname(__file__)
        self.DATA_DIR = os.path.join(self.basedir, app.config['DATA_DIRECTORY'])
        self.testing = app.config['TESTING']

        if not os.path.isdir(self.DATA_DIR):
            os.mkdir(self.DATA_DIR)

    def readFile(self, name, dir=None):
        """Load a json file from disk

        Args:
            name (str): filename, no extension
            dir (str, optional): Sub directory to use. Defaults to None.
        Returns:
            dict: dict generated from json file on disk
        """
        try:
            with open(self.getPath(name, dir), 'r') as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            # LOG EVENT: FILE NOT FOUND
            return None

    def writeFile(self, name, data, dir=None):
        """Write a json file to disk

        Args:
            name (str): filename, no extension
            data (dict): data to write
            dir (str, optional): Name of directory to write to. Defaults to None.
        """
        if dir:
            if not os.path.isdir(os.path.join(self.DATA_DIR, dir)):
                os.makedirs(os.path.join(self.DATA_DIR, dir))

        with open(self.getPath(name, dir), 'w') as file:
            json.dump(data, file)

    def deleteFile(self, name, dir=None):
        """Deletes the file specified from disk

        Args:
            name (str): filename, no extension
            dir (str, optional): Name of directory that file is in. Defaults to None.
        """
        path = self.getPath(name, dir)
        if self.file_exists(name, dir='games'):
            os.remove(path)
        else:
            print("File not found")

    def file_exists(self, name, dir=None):
        """Checks if the file specified exists

        Args:
            name (str): filename, no extension
            dir (str, optional): Name of directory to look in. Defaults to None.

        Returns:
            bool: True if file exists, false if not
        """
        return os.path.isfile(self.getPath(name, dir))

    def getPath(self, name, dir=None, filetype='.json'):
        """Joins the path to the file using system separators

        Args:
            name (str): filename
            dir (str, optional): Name of directory. Defaults to None.
            filetype (str, optional): Extension of file. Defaults to '.json'.

        Returns:
            str: String of path to file
        """
        if dir:
            if filetype:
                return os.path.join(self.DATA_DIR, dir, '{}{}'.format(name, filetype))
            else:
                return os.path.join(self.DATA_DIR, dir, '{}'.format(name))
        else:
            if filetype:
                return os.path.join(self.DATA_DIR, '{}{}'.format(name, filetype))
            else:
                return os.path.join(self.DATA_DIR, '{}'.format(name))

    def remove_all(self, testing=False):
        """Remove all data: ONLY USED FOR TESTING, checks config as well.

        Args:
            testing (bool, optional): Are you testing. Defaults to False.
        """
        if testing:  # Sanity check, should never be used in production
            if self.testing:  # Second check if testing in config
                # Remove Games
                for filename in os.listdir(os.path.join(self.DATA_DIR, 'games')):
                    path = self.getPath(filename, dir='games', filetype=None)
                    if os.path.isfile(path):
                        os.remove(path)
                for filename in os.listdir(os.path.join(self.DATA_DIR, 'users')):
                    path = self.getPath(filename, dir='users', filetype=None)
                    if os.path.isfile(path):
                        os.remove(path)
                for filename in os.listdir(self.DATA_DIR):
                    path = self.getPath(filename, filetype=None)
                    if os.path.isfile(path):
                        os.remove(path)
