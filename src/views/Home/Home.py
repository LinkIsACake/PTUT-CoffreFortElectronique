import sys

import PyQt5

sys.path.append('..')

from src.controllers.MainController import MainController

import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QDropEvent
from PyQt5.QtWidgets import QAction, qApp, QPushButton, QVBoxLayout, QLabel, QDesktopWidget, QSizePolicy, QGridLayout, \
    QWidget, QListWidget, QMessageBox

from views.Login import Login

from models.UserSession import UserSession
from Utils.Logger import Logger


class FileListWidget(QListWidget):

    def __init__(self,parent=None):
        super(FileListWidget, self).__init__(parent)

    def add_file(self, file: str):
        self.addItem(file)

    def remove_file(self):
        self.takeItem(self.currentRow())


class Home(QWidget, Logger):
    controller: MainController

    session_user : UserSession

    label: QLabel
    label_path: QLabel

    layout: QGridLayout
    file_list: FileListWidget

    button_send: QPushButton
    button_delete: QPushButton

    def __init__(self, controller, *args, **kwargs):
        Logger.__init__(self)

        QWidget.__init__(self, *args, **kwargs)

        self.controller = controller
        self.setAcceptDrops(True)

        self.initUI()
        self.notify()

    def dropEvent(self, event):
        files = [file.toLocalFile() for file in event.mimeData().urls()]
        for file in files:
            try:
                self.file_list.add_file(file)
            except Exception as err:
                print(err)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def notify(self, **kwargs):
        if kwargs.get("connected", False) and kwargs.get("username", False):
            self.session_user = kwargs.get("session_user", None)
            self.label.setText("Bonjour " + self.session_user.username + "\n Deposez votre fichier à protéger ici !")
        else:
            self.label.setText("Connectez vous")

        if kwargs.get("sending_file_status", False):
            QMessageBox.about(self, "Succes", "Envoi des fichiers reussi ! ")

    def initUI(self):

        self.label = QLabel("", self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignCenter)

        self.file_list = FileListWidget(self)
        self.button_delete = QPushButton("supprimer")
        self.button_delete.pressed.connect(self.file_list.remove_file)

        self.button_send = QPushButton("envoyer")
        self.button_send.pressed.connect(self.send_files)

        self.layout = QGridLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.file_list)

        self.layout.addWidget(self.button_delete)
        self.layout.addWidget(self.button_send)

        self.setLayout(self.layout)
        self.show()

    def send_files(self):

        files_to_send = []

        for index in range(self.file_list.count()):
            files_to_send.append(self.file_list.item(index).text())

        self.controller.send_files(files_to_send)
