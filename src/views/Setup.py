from PyQt5.QtWidgets import QPushButton, QLineEdit, QMessageBox, QGridLayout, QLabel, QListWidget
from PyQt5 import QtWidgets
from PyQt5 import uic

from src.controllers import MainController
from src.assets.Label import Label

class Setup(QtWidgets.QDialog):

    controller : MainController
    
    def __init__(self,controller,parent=None):
        super().__init__(parent)
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        dialog = uic.loadUi("views/Setup.ui", self)
        dialog.show()

    