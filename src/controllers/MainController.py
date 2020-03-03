import sys
import os
sys.path.append('..')

from dotenv import load_dotenv
load_dotenv()

from views.Home import Home
from views.Login import Login

from .LoginController import LoginController
from .FileController import FileController

class MainController:
    connected: bool
    loginController : LoginController
    fileController : FileController

    destinationPath = os.getenv("FILE_DESTINATION")

    observers: []

    def __init__(self):
        self.loginController = LoginController()
        self.connected = False

        self.observers = [Login.Login(self)]

    def notify(self, **kwargs):
        for observer in self.observers:
            observer.notify(**kwargs)

    def login(self, username, password):
        wrong_credential = False
        if self.loginController.login(username, password):
            self.connected = True
            self.observers.append(Home.Home(self))
        else:
            wrong_credential = True

        self.notify(connected=self.connected, wrong_credential=wrong_credential)

    def register(self, username, password):
        self.loginController.register(username, password)
        self.notify()

    def saveFile(self, path):
        result = self.fileController.saveFile(path, self.destinationPath)
        return result

    def getFile(self, path):
        result = self.fileController.getFile(path,self.destinationPath)
