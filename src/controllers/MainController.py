import sys
import os

sys.path.append('..')

from views import SendFileManager
from views import Login
from views import Home

from models.User import User
from models.UserSession import UserSession

from .LoginController import LoginController
from .FileController import FileController

from Utils.Logger import Logger
from nacl import pwhash,exceptions


class MainController(Logger):
    connected: bool
    loginController: LoginController
    fileController: FileController

    session: UserSession

    destinationPath = "../ressource/"

    observers: []

    def __init__(self):
        Logger.__init__(self)

        self.loginController = LoginController()
        self.fileController = FileController(self.destinationPath)
        self.connected = False
        self.observers = [Login.Login(self)]
        self.user = None

    def notify(self, **kwargs):
        """
        Notify all observer

        :param kwargs: arguments to notify
        """
        for observer in self.observers:
            observer.notify(**kwargs)

    def create_home(self, username: str):
        self.logger.debug("login_ok, create Home")
        self.connected = True
        self.observers.pop()
        self.session = UserSession(username, self.destinationPath + username)
        self.observers.append(Home.Home(self))

        return True

    def login(self, username, password):
        self.logger.debug("login")

        wrong_credential = False

        if username != "" and password != "":

            if self.loginController.login(username, password):
                hash_password = pwhash.scrypt.str(password.encode('utf8'))

                self.user = User(username, hash_password)
                self.create_home(username)
            else:
                wrong_credential = True
        else:
            wrong_credential = True

        self.notify(connected=self.connected,
                    wrong_credential=wrong_credential,
                    username=username)

    def register(self, username, password):
        """
        Register new user

        :param username:
        :param password:
        """

        self.logger.debug("register")

        wrong_input = False
        result = False
        path_exist = False

        if username != "" and password != "":
            if self.loginController.user_exist(username):
                self.notify(user_exist=True)
            else:
                if not os.path.isdir(self.destinationPath + username):
                    os.mkdir(self.destinationPath + username)
                    result = self.loginController.register(username, pwhash.scrypt.str(password.encode('utf8')))
                    self.notify(register=True)
                else:
                    self.notify(path_exist=True)
        else:
            self.notify(wrong_input=True)

    def saveFile(self, path):
        self.logger.debug("saveFile")

        """
        Send a order of encryption for a file

        :param path: path of the file
        """
        self.logger.debug("saveFile")

        result = False
        if path:
            result = self.fileController.saveFile(path, self.user)
        return result

    def getFile(self, path):
        self.logger.debug("getFile" + str(path))
        result = self.fileController.getFile(path, self.user)

    def send_files(self, files_to_send: []):
        """
        Send list of file to encrypt

        :param files_to_send: list of path of file to encrypt
        """
        self.logger.debug("send_files")

        self.logger.debug(files_to_send)
        for file in files_to_send:
            self.saveFile(file)
        self.notify(sending_file_status=True)

    def get_files(self) -> []:

        files_list = []

        for root, dirs, files in os.walk(self.session.path):
            for file in files:
                files_list.append(file)

        return files_list
