import sys
sys.path.append(".")
from PyQt5.QtWidgets import QApplication
from src.controllers.MainController import MainController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainController = MainController()
    sys.exit(app.exec_())