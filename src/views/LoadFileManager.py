from PyQt5.QtWidgets import QPushButton, QLabel, QGridLayout, \
    QWidget, QListWidget, QMessageBox

from src.Utils.Logger import Logger
from src.controllers import MainController
from src.assets.Label import Label


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

    button_load: QPushButton
    button_delete: QPushButton

    files = [str]

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
            if file[0] != "_":
                self.file_list.add_file(file)
        self.logger.info("update_list_done")

    def delete_file(self):
        pass

    def get_file(self):
        file = self.file_list.takeItem(self.file_list.currentRow())
        if file:
            self.controller.getFile(file.text())
        else:
            QMessageBox.about(self, Label.INFO, Label.NO_FILES_TO_SEND)

    def initUI(self):
        self.label = QLabel(Label.FILES_PROTECTED, self)

        self.file_list = FileListWidget(self)
        self.button_load = QPushButton(Label.LOAD)
        self.button_delete = QPushButton(Label.DELETE)

        self.layout = QGridLayout()
        self.layout.addWidget(self.label, 0, 0)
        self.layout.addWidget(self.file_list, 1, 0)

        self.layout.addWidget(self.button_load, 2, 0)
        self.layout.addWidget(self.button_delete, 3, 0)

        self.button_delete.pressed.connect(self.delete_file)
        self.button_load.pressed.connect(self.get_file)

        self.setLayout(self.layout)
        self.show()
