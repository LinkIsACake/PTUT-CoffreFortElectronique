import sys

from PyQt5.QtWidgets import QPlainTextEdit, QPushButton, QLineEdit, QMessageBox

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

    def notify(self, **kwargs):
        if kwargs.get("connected", False):
            self.close()
        else:
            if kwargs.get("register", False):
                QMessageBox.about(self ,"Inscription", "Inscription reussit")
            else:
                QMessageBox.about(self ,"Erreur", "Compte déjâ existant")

            if kwargs.get("wrong_credential",False):
                QMessageBox.about(self ,"Erreur", "Mot de passe ou Nom d'utilisateur incorrect")

            if kwargs.get("path_exist", False):
                QMessageBox.about(self ,"Erreur", "Un dossier correspond déjâ à se nom utilisateur mais il n'est pas enregisté, supprimer le dossier")
            if kwargs.get("wrong_input",False):
                QMessageBox.about(self ,"Erreur", "Nom d'utilisateur ou mot de passe incorrect")
