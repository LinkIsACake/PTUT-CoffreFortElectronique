import sys

from PyQt5.QtWidgets import QPlainTextEdit

from src.controllers import MainController

sys.path.append('..')



from PyQt5 import uic
from PyQt5.uic.Compiler.qtproxies import QtGui
from PyQt5 import (QtWidgets, QtCore)



class Login(QtWidgets.QDialog):
    controller : MainController

    username_input : QPlainTextEdit

    def __init__(self,controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        dialog = uic.loadUi("views/Login/Login.ui", self)
        dialog.show()

        self.login_button.pressed.connect(self.login)

    def login(self):
        self.controller.login(self.username_input.toPlainText(),self.password_input.toPlainText())

    def notify(self):
        pass
# etc
