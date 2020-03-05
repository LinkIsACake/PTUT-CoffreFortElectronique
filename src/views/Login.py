import sys

from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QPlainTextEdit, QPushButton, QLineEdit, QMessageBox, QGridLayout, QLabel, QListWidget, \
    QFrame

sys.path.append('..')

from src.controllers import MainController

from PyQt5 import uic
from PyQt5.uic.Compiler.qtproxies import QtGui
from PyQt5 import (QtWidgets, QtCore)


class UserList(QListWidget):

    def __init__(self, parent=None):
        super(UserList, self).__init__(parent)

    def add_user(self, user: str):
        self.addItem(user)


class Login(QtWidgets.QDialog):
    layout: QGridLayout

    controller: MainController

    login_button: QPushButton
    register: QPushButton
    password_input: QLineEdit
    username_input: QLineEdit
    users: []
    user_list: UserList

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        # dialog = uic.loadUi("views/Login.ui", self)
        # dialog.show()

        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 300, 250, 150)
        self.layout = QGridLayout()
        self.layout.setColumnStretch(10, 10)
        self.login_button = QPushButton("Connexion")
        self.register_button = QPushButton("Inscription")

        self.login_button.pressed.connect(self.login)
        self.register_button.pressed.connect(self.register)

        self.username_input = QLineEdit()

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.layout.addWidget(QLabel("Nom d'utilisateur"), 0, 0)

        self.layout.addWidget(QLabel("Mot-de-passe"), 1, 0)

        self.layout.addWidget(self.username_input, 0, 1)
        self.layout.addWidget(self.password_input, 1, 1)

        self.layout.addWidget(self.login_button, 2, 0)
        self.layout.addWidget(self.register_button, 2, 1)

        self.layout.addWidget(QLabel("Utilisateurs existants"), 0, 3)

        self.user_list = UserList()
        self.user_list.clicked.connect(self.select_user)

        self.update_list_user()
        self.layout.addWidget(self.user_list, 1, 3)
        self.setLayout(self.layout)
        self.show()

    def select_user(self):
        user_selected = self.user_list.selectedItems()[0]

        self.username_input.setText(user_selected.text())

    def update_list_user(self):
        self.users = self.controller.get_users()

        self.user_list.clear()
        for user in self.users:
            self.user_list.add_user(user)

    def register(self):
        self.controller.register(self.username_input.text(), self.password_input.text())

    def login(self):
        self.controller.login(self.username_input.text(), self.password_input.text())

    def connected(self):
        self.close()

    def register_ok(self):
        QMessageBox.about(self, "Inscription", "Inscription réussie")

    def wrong_credential(self):
        QMessageBox.about(self, "Erreur", "Mot-de-passe ou Nom d'utilisateur incorrect")

    def path_exist(self):
        QMessageBox.about(self, "Erreur",
                          "Un dossier correspond déjâ à ce nom utilisateur mais il n'est pas enregisté, veuillez supprimer le dossier")

    def wrong_input(self):
        QMessageBox.about(self, "Erreur", "Mot-de-passe ou Nom d'utilisateur incorrect")

    def notify(self, **kwargs):
        if kwargs.get("connected", False):
            self.register_ok()
            self.close()
        else:
            if kwargs.get("register", False):
                self.register_ok()
            else:
                QMessageBox.about(self, "Compte déjâ existant")
            if kwargs.get("path_exist", False):
                self.path_exist()
            if kwargs.get("wrong_credential", False):
                self.wrong_credential()
            if kwargs.get("wrong_input", False):
                self.wrong_input()
        self.update_list_user()
