import sys


sys.path.append('..')

from views.Home import Home
from views.Login import Login
from Dao.Dao import Dao


class MainController:

    connected : bool
    observers : []
    dao :
    def __init__(self):
        self.connected = False
        self.observers = [Home.Home(self),Login.Login(self)]

    def notify(self):
        for observer in self.observers:
            observer.notify()

    def login(self, username, password):
        self.connected = True
        self.notify()

