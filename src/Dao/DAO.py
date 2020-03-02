from .DbHelper import DbHelper

class DAO:
    database = None

    def __init__(self, path:str):
        self.database = DbHelper(path)

    def close(self):
        self.database.close()
