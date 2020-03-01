from .DbHelper import DbHelper

class DAO:
    database = None

    def __init__(self):
        self.database = DbHelper()

    def close(self):
        self.database.close()