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
    button_delete : QPushButton

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

    def delete_file(self):
        pass

    def get_file(self):
        file = self.file_list.takeItem(self.file_list.currentRow())
        if file:
            self.controller.getFile(file.text())
        else:
            QMessageBox.about(self,"Info", "Aucun fichier à envoyer")

    def initUI(self):
        self.label = QLabel("Vos fichiers protegés", self)


        self.file_list = FileListWidget(self)
        self.button_load = QPushButton("Charger")
        self.button_delete = QPushButton("Supprimer")

        self.layout = QGridLayout()
        self.layout.addWidget(self.label,0,0)
        self.layout.addWidget(self.file_list,1,0)

        self.layout.addWidget(self.button_load,2,0)
        self.layout.addWidget(self.button_delete,3,0)

        self.button_delete.pressed.connect(self.delete_file)
        self.button_load.pressed.connect(self.get_file)

        self.setLayout(self.layout)
        self.show()
