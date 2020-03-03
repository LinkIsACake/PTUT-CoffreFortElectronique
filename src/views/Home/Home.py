import sys

sys.path.append('..')

from src.controllers.MainController import MainController

import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QDropEvent
from PyQt5.QtWidgets import QAction, qApp, QPushButton, QVBoxLayout, QLabel, QDesktopWidget, QSizePolicy, QGridLayout, \
    QWidget, QListWidget

from views.Login import Login

from Utils.Logger import Logger


class Home(QWidget, Logger):
    controller: MainController
    label: QLabel
    label_path: QLabel

    layout: QGridLayout
    file_list: QListWidget

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
        files = event.mimeData().urls()
        for file in files:
            try:
                self.file_list.addItem(file.toString())
            except Exception as err:
                print(err)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def notify(self, **kwargs):
        if kwargs.get("connected", False) and kwargs.get("username", False):
            username = kwargs.get("username", "")
            self.label.setText("Bonjour " + username + "\n Deposer votre fichier à proteger ici !")
        else:
            self.label.setText("Connecter vous")

    def initUI(self):

        self.label = QLabel("", self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignCenter)

        self.file_list = QListWidget(self)
        self.button_delete = QPushButton("supprimer")
        self.button_delete.pressed.connect(self.delete_file)

        self.button_send = QPushButton("envoyer")

        self.layout = QGridLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.file_list)

        self.layout.addWidget(self.button_delete)
        self.layout.addWidget(self.button_send)

        self.setLayout(self.layout)
        self.show()

    def delete_file(self):
        self.file_list.takeItem(self.file_list.currentRow())

    def update_file_manager(self):
        pass
