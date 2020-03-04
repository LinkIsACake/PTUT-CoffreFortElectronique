import sys

sys.path.append('..')

from controllers import MainController

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, qApp, QPushButton, QVBoxLayout, QLabel, QDesktopWidget, QSizePolicy, QGridLayout, \
    QWidget, QListWidget, QMessageBox

from Utils.Logger import Logger


class FileListWidget(QListWidget):

    def __init__(self, parent=None):
        super(FileListWidget, self).__init__(parent)

    def add_file(self, file: str):
        self.addItem(file)

    def remove_file(self):
        self.takeItem(self.currentRow())


class LoadFileManager(QWidget, Logger):
    controller: MainController

    label: QLabel
    label_path: QLabel

    layout: QGridLayout
    file_list: FileListWidget

    button_load : QPushButton
    files = []

    def __init__(self, controller, *args, **kwargs):
        Logger.__init__(self)

        QWidget.__init__(self, *args, **kwargs)

        self.controller = controller

        self.initUI()
        self.update_list()

    def update_list(self):
        self.files = self.controller.get_files()

        self.file_list.clear()

        for file in self.files:
            self.file_list.add_file(file)

    def initUI(self):
        self.label = QLabel("Vos fichiers protegés", self)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignCenter)

        self.file_list = FileListWidget(self)
        self.button_load = QPushButton("Charger")
        self.layout = QGridLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.file_list)
        self.layout.addWidget(self.button_load)

        self.setLayout(self.layout)
        self.show()
