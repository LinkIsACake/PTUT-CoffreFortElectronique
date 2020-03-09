import os

from src.views import Login
from src.views import Home
from src.views import Setup

from src.models.User import User
from src.models.UserSession import UserSession

from src.controllers.LoginController import LoginController
from src.controllers.FileController import FileController
from src.controllers.FtpController import FtpController

from src.Utils.Logger import Logger

from nacl import pwhash


class MainController(Logger):
    connected: bool
    loginController: LoginController
    fileController: FileController
    ftpController: FtpController

    session: UserSession

    destinationPath = "ressource/"

    observers: []

    def __init__(self):
        Logger.__init__(self)

        self.loginController = LoginController()
        self.fileController = FileController(self.destinationPath)
        self.ftpController = None
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
        """
        Init UserHome when connected

        :param username: name of the user
        """
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

    def logout(self):
        self.observers.pop()
        self.session = None
        self.observers.append(Login.Login(self))

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

    def save_file(self, path, delete_after_upload: bool):
        self.logger.debug("saveFile")
        """
        Send a order of encryption for a file

        :param path: path of the file
        """
        self.logger.debug("saveFile")

        result = False
        if path:
            result = self.fileController.save_file(path, self.user)
            if result and delete_after_upload:
                os.remove(path)
        return result

    def get_file(self, path):
        """
        Send a request to decrypt file
        :param path : path of the file to decrypt

        """
        self.logger.debug("getFile" + str(path))
        result = self.fileController.get_file(path, self.user)
        if result:
            self.notify(load_file_succes=True)

    def send_files(self, files_to_send: [], delete_after_upload: bool):
        """
        Send list of file to encrypt

        :param files_to_send: list of path of file to encrypt
        """
        self.logger.debug("send_files")
        self.logger.debug(files_to_send)

        if self.ftpController is not None:
            for file in files_to_send:
                self.ftpController.upload_file(file)
        else:
            for file in files_to_send:
                self.save_file(file, delete_after_upload)

        self.notify(sending_file_status=True)

    def get_files_list(self) -> []:
        """
        Get lists of all existing files in the user folder

        :return list of file name
        """
        self.logger.info("get_files")
        if self.ftpController is not None:
            ftpFiles = self.ftpController.list_directory()
            if ftpFiles:
                return ftpFiles
            else:
                return ["Emplacement vide"]
        else:
            files_list = []
            for root, dirs, files in os.walk(self.session.path):
                for file in files:
                    files_list.append(file)

            return files_list

    def get_users(self):
        """
        Get lists of all existing users

        :return list of username
        """
        return self.loginController.get_users()

    def setup(self):
        self.observers.append(Setup.Setup(self))

    def create_ftp_connection(self, url, username, password):
        self.ftpController = FtpController(url, username, password)
        self.observers.pop()
        self.notify()

    def end_ftp_connection(self):
        self.ftpController.quit_session()
        self.ftpController = None
