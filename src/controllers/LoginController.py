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
        self.logger.debug("login " + username)
        result = False
        if self.user_exist(username):
            result = self.dao.checkCredentials(username, password)
        return result

    def register(self, username: str, password: str):
        self.logger.debug("register " + username)
        return self.dao.createUser(username, password)

    def user_exist(self, username: str):
        self.logger.debug("user_exist ")
        return self.dao.userExist(username)

    def get_users(self) -> []:
        return self.dao.fetchAllUsers()
