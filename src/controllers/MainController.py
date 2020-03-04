import sys
import os

sys.path.append('..')

from dotenv import load_dotenv

load_dotenv()

from views.Home import Home
from views.Login import Login

from models.User import User
from models.UserSession import UserSession

from .LoginController import LoginController
from .FileController import FileController

from Utils.Logger import Logger


class MainController(Logger):
    connected: bool
    loginController: LoginController
    fileController: FileController

    session: User

    destinationPath = "../ressource/"

    observers: []

    def __init__(self):
        Logger.__init__(self)

        self.loginController = LoginController()
        self.fileController = FileController(self.destinationPath)
        self.connected = False
        self.session = None
        self.observers = [Login.Login(self)]

    def notify(self, **kwargs):
        """
        Notify all observer

        :param kwargs: arguments to notify
        """
        for observer in self.observers:
            observer.notify(**kwargs)

    def create_home(self,username : str,password : str):
        self.logger.debug("login_ok, create Home")
        self.connected = True
        self.session = User(username, password)
        self.observers.pop()
        self.observers.append(Home.Home(self))
        return UserSession(username, self.destinationPath + username)

    def login(self, username, password):
        self.logger.debug("login")

        wrong_credential = False

        session_user = None

        if username != "" and password != "":
            if self.loginController.login(username, password):
                session_user = self.create_home(username, password)
            else:
                wrong_credential = True
        else:
            wrong_credential = True

        self.notify(connected=self.connected,
                    wrong_credential=wrong_credential,
                    username=username,
                    session_user=session_user)

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
                result = False
            else:
                if not os.path.isdir(self.destinationPath + username):
                    os.mkdir(self.destinationPath + username)
                    result = self.loginController.register(username, password)
                else:
                    path_exist = True
        else:
            wrong_input = True

        self.notify(register=result, path_exist=path_exist, wrong_input=wrong_input)

    def saveFile(self, path):
        self.logger.debug("saveFile")

        """
        Send a order of encryption for a file

        :param path: path of the file
        """
        self.logger.debug("saveFile")

        result = False
        if path:
            result = self.fileController.saveFile(path, self.session)
        return result

    def getFile(self, path):
        self.logger.debug("getFile")

        result = self.fileController.getFile(path, self.session)

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
