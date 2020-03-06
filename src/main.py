import logging
import sys

from PyQt5.QtWidgets import QApplication
from src.controllers import MainController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainController = MainController.MainController()
    sys.exit(app.exec_())