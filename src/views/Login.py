from PyQt5.QtWidgets import QPushButton, QLineEdit, QMessageBox, QGridLayout, QLabel, QListWidget
from PyQt5 import QtWidgets

from src.controllers import MainController
from src.assets.Label import Label


class UserList(QListWidget):

    def __init__(self, parent=None):
        super(UserList, self).__init__(parent)

    def add_user(self, user: str):
        self.addItem(user)


class Login(QtWidgets.QDialog):
    layout: QGridLayout

    controller: MainController

    login_button: QPushButton
    register_button: QPushButton

    register: QPushButton
    password_input: QLineEdit
    username_input: QLineEdit
    users: []
    user_list: UserList

    def __init__(self, controller, parent=None):
        super().__init__(parent)

        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 300, 250, 150)
        self.layout = QGridLayout()
        self.layout.setColumnStretch(10, 10)
        self.login_button = QPushButton(Label.LOGIN_BUTTON)

        self.register_button = QPushButton(Label.REGISTRATION_BUTTON)

        self.login_button.pressed.connect(self.login)
        self.register_button.pressed.connect(self.register)

        self.username_input = QLineEdit()

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.layout.addWidget(QLabel(Label.LOGIN_INPUT_USERNAME), 0, 0)

        self.layout.addWidget(QLabel(Label.REGISTRATION_BUTTON), 1, 0)

        self.layout.addWidget(self.username_input, 0, 1)
        self.layout.addWidget(self.password_input, 1, 1)

        self.layout.addWidget(self.login_button, 2, 0)
        self.layout.addWidget(self.register_button, 2, 1)

        self.layout.addWidget(QLabel(Label.EXISTING_USERS), 0, 3)

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

    def notif_about_info(self, message: str):
        QMessageBox.about(self, Label.INFO, message)

    def notif_about_error(self, message):
        QMessageBox.about(self, Label.ERROR, message)

    def notify(self, **kwargs):
        if kwargs.get("connected", False):
            self.close()
        else:
            if kwargs.get("register", False):
                self.notif_about_info(Label.REGISTER_DONE)
            else:
                self.notif_about_error(Label.ACCOUNT_EXISTING)
            if kwargs.get("path_exist", False):
                self.notif_about_error(Label.PATH_EXIST)
            if kwargs.get("wrong_credential", False):
                self.notif_about_error(Label.WRONG_CREDENTIAL)
            if kwargs.get("wrong_input", False):
                self.notif_about_error(Label.WRONG_INPUT)
        self.update_list_user()
