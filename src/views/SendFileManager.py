import sys

sys.path.append('..')

from src.controllers import MainController


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, qApp, QPushButton, QVBoxLayout, QLabel, QDesktopWidget, QSizePolicy, QGridLayout, \
    QWidget, QListWidget, QMessageBox

from Utils.Logger import Logger



class FileListWidget(QListWidget):

    def __init__(self,parent=None):
        super(FileListWidget, self).__init__(parent)

    def add_file(self, file: str):
        self.addItem(file)

    def remove_file(self):
        self.takeItem(self.currentRow())


class SendFileManager(QWidget, Logger):
    controller: MainController

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
        if kwargs.get("sending_file_status", False):
            QMessageBox.about(self, "Succes", "Envoi des fichiers réussi ! ")

    def initUI(self):

        self.label = QLabel("Protéger de nouveaux fichiers", self)
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
