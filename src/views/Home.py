import sys

sys.path.append('..')

from controllers import MainController

import PyQt5


from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QDropEvent
from PyQt5.QtWidgets import QAction, qApp, QPushButton, QVBoxLayout, QLabel, QDesktopWidget, QSizePolicy, QGridLayout, \
    QWidget, QListWidget, QMessageBox

from . import SendFileManager
from . import LoadFileManager

from Utils.Logger import Logger


class Home(QWidget, Logger):
    controller: MainController
    layout: QGridLayout

    sendFileManager: SendFileManager
    LoadFileManager: LoadFileManager

    button_load: QPushButton
    button_send: QPushButton

    def __init__(self, controller, *args, **kwargs):
        Logger.__init__(self)

        QWidget.__init__(self, *args, **kwargs)

        self.controller = controller

        self.initUI()
        self.notify()

    def notify(self, **kwargs):
        self.loadFileManager.update_list()

    def initUI(self):
        self.layout = QGridLayout()
        self.layout.setColumnStretch(2, 2)

        self.sendFileManager = SendFileManager.SendFileManager(self.controller)
        self.loadFileManager = LoadFileManager.LoadFileManager(self.controller)

        self.layout.addWidget(self.sendFileManager, 0, 0)
        self.layout.addWidget(self.loadFileManager, 0, 1)

        self.setLayout(self.layout)
        self.show()
