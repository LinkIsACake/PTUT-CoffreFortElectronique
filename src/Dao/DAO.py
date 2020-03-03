from .DbHelper import DbHelper

class DAO:
    database = None
    init : bool
    def __init__(self, path:str):
        self.init = DbHelper.check_file(path)
        self.database = DbHelper(path)

    def close(self):
        self.database.close()
