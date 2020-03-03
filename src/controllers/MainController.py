import sys

sys.path.append('..')

from views.Home import Home
from views.Login import Login

from .LoginController import LoginController
from .FileController import FileController

class MainController:
    connected: bool
    loginController : LoginController
    fileController : FileController

    destinationPath = "../Files"

    observers: []

    def __init__(self):
        self.loginController = LoginController()
        self.connected = False

        self.observers = [Home.Home(self), Login.Login(self)]

    def notify(self):
        for observer in self.observers:
            observer.notify()

    def login(self, username, password):
        if self.loginController.login(username, password):
            self.connected = True
        self.notify()

    def register(self, username, password):
        self.loginController.register(username, password)
        self.notify()

    def saveFile(self, path):
        result = self.fileController.saveFile(path,destinationPath, self.user)
        return result

    def getFile(self, path):
        result = self.fileController.getFile(path,destinationPath, self.user)
