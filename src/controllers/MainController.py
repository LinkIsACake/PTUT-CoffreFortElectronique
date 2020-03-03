import sys
import os


sys.path.append('..')

from dotenv import load_dotenv
load_dotenv()

from views.Home import Home
from views.Login import Login

from models.User import User

from .LoginController import LoginController
from .FileController import FileController

from Utils.Logger import Logger

class MainController(Logger):
    connected: bool
    loginController : LoginController
    fileController : FileController

    session : User

    destinationPath = os.getenv("FILE_DESTINATION")

    observers: []

    def __init__(self):
        Logger.__init__(self)

        self.loginController = LoginController()
        self.fileController = FileController("../ressource/")
        self.connected = False
        self.session = None
        self.observers = [Login.Login(self)]

    def notify(self, **kwargs):
        for observer in self.observers:
            observer.notify(**kwargs)

    def login(self, username, password):
        wrong_credential = False
        if self.loginController.login(username, password):
            self.connected = True
            self.session = User(username, password)
            self.observers.append(Home.Home(self))
        else:
            wrong_credential = True

        self.notify(connected=self.connected, wrong_credential=wrong_credential, username=username)

    def register(self, username, password):
        result = self.loginController.register(username, password)
        self.notify(register=result)

    def saveFile(self, path):
        result = self.fileController.saveFile(path, self.session)
        return result

    def getFile(self, path):
        result = self.fileController.getFile(path,self.destinationPath)

    def send_files(self, files_to_send : []):
        self.logger.debug(files_to_send)
        for file in files_to_send:
            self.saveFile(file)
        self.notify(sending_file_status=True)
