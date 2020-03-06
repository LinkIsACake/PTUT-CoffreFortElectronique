from PyQt5.QtWidgets import QPushButton, QGridLayout, \
    QWidget, QMessageBox

from src.Utils.Logger import Logger
from src.controllers import MainController
from src.views.LoadFileManager import LoadFileManager
from src.views.SendFileManager import SendFileManager

from src.assets.Label import Label

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
        if kwargs.get("load_file_succes", False):
            QMessageBox.about(self, Label.INFO, Label.FILES_LOAD_SUCCES)

    def logout(self):
        self.close()
        self.controller.logout()

    def setup(self):
        self.controller.setup()

    def initUI(self):
        self.layout = QGridLayout()
        self.layout.setColumnStretch(3, 3)
        self.button_config = QPushButton("Paramètres")
        self.layout.addWidget(self.button_config, 3,0)
        self.sendFileManager = SendFileManager(self.controller)
        self.loadFileManager = LoadFileManager(self.controller)
        self.button_logout = QPushButton(Label.LOGOUT)
        self.button_logout.clicked.connect(self.logout)
        self.button_config.clicked.connect(self.setup)

        self.layout.addWidget(self.sendFileManager, 0, 0)
        self.layout.addWidget(self.loadFileManager, 0, 1)
        self.layout.addWidget(self.button_logout, 2, 0)

        self.setLayout(self.layout)
        self.show()
