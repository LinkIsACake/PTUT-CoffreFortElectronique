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
        dialog = uic.loadUi("src/views/Setup.ui", self)
        dialog.show()

        self.cheminLocalLineEdit.setText(self.controller.destinationPath)
        self.pushButton_validate.pressed.connect(self.validate_changes)
        self.pushButton_cancel.pressed.connect(self.cancel_changes)

    def cancel_changes(self):
        self.close()

    def validate_changes(self):
        if self.radioButton_remote.isChecked():
            ftpUrl = self.uRLDistanteFtpLineEdit.text()
            ftpUsername = self.nomDUtilisateurLineEdit.text()
            ftpPassword = self.motDePasseLineEdit.text()

            self.controller.create_ftp_connection(ftpUrl,ftpUsername,ftpPassword)
        else:
            localPath = self.cheminLocalLineEdit.text()
            self.controller.destinationPath = localPath

    #valider: appeler fonction configure du mainController
    #passer en paramètres
    #modifier filemanager pour mode distant et mode local