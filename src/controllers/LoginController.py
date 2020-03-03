import sys

sys.path.append('..')
import nacl
from Dao.UserDAO import UserDAO
from Utils.Logger import Logger


class LoginController(Logger):
    dao: UserDAO

    def __init__(self):
        Logger.__init__(self)
        self.dao = UserDAO()

    def login(self, username: str, password: str):
        self.logger.debug("login")
        return self.dao.checkCredentials(username, password)

    def register(self, username: str, password: str):
        self.logger.debug("register")
        self.dao.createUser(username, password)
