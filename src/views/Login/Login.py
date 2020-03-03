import sys

from PyQt5.QtWidgets import QPlainTextEdit, QPushButton, QLineEdit

from src.controllers import MainController

sys.path.append('..')

from PyQt5 import uic
from PyQt5.uic.Compiler.qtproxies import QtGui
from PyQt5 import (QtWidgets, QtCore)


class Login(QtWidgets.QDialog):
    controller: MainController

    login_button: QPushButton
    register: QPushButton

    password_input: QLineEdit
    username_input: QLineEdit

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        dialog = uic.loadUi("views/Login/Login.ui", self)
        dialog.show()

        self.login_button.pressed.connect(self.login)
        self.register_button.pressed.connect(self.register)
    def register(self):
        self.controller.register(self.username_input.text(), self.password_input.text())

    def login(self):
        self.controller.login(self.username_input.text(), self.password_input.text())

    def notify(self):
        pass
# etc
