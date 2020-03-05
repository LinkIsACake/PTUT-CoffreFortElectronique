import os


class UserSession:

    username: str
    path: str

    files : []

    def __init__(self, username: str, path : str):
        self.username = username
        self.path = path
        self.files = []

    def list_file(self):
        if os.path.isdir(self.path):
            for root, dirs, files in os.walk(self.path):
                self.files.append(files)
