import sys

sys.path.append('..')

from Dao.UserDAO import UserDAO


class LoginController:
    dao: UserDAO

    def __init__(self):
        self.dao = UserDAO()

    def login(self, username, password):
        result = self.dao.checkCredentials(username, password)
        return result

    def register(self, username, password):
        self.dao.createUser(username, password)
