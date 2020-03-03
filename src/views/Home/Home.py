import sys

sys.path.append('..')

from src.controllers.MainController import MainController


import sys
import json
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, qApp, QPushButton, QVBoxLayout, QLabel, QDesktopWidget, QSizePolicy, QGridLayout, \
    QWidget

from views.Login import Login


class Home(QWidget):
    controller: MainController
    label: QLabel
    layout: QGridLayout

    def __init__(self, controller, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        self.controller = controller

        self.initUI()
        self.notify()

    def notify(self):
        if self.controller.connected:
            self.label.setText("Vous etez connectez")
        else:
            self.label.setText("Connecter vous")

    def initUI(self):

        self.label = QLabel("", self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignCenter)

        self.layout = QGridLayout()
        self.layout.addWidget(self.label, 0, 0)

        self.setLayout(self.layout)
        self.show()

    def init_file_manager(self):
        pass
