from .DbHelper import DbHelper
from Utils.Logger import Logger

class DAO(Logger):
    database = None
    init : bool

    def __init__(self, path:str):
        Logger.__init__(self)

        self.init = DbHelper.check_file(path)
        self.database = DbHelper(path)

    def close(self):
        self.database.close()
