import logging
import sys

from PyQt5.QtWidgets import QApplication
from controllers import MainController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainController = MainController()
    sys.exit(app.exec_())