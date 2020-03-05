import os
import sys

sys.path.append('..')

from EncryptCore import FileEncryptor
from EncryptCore.beforeImplemented import *

import logging
from models.File import File
from models.User import User


class FileController:
    destinationPath: str
    logger: logging

    def __init__(self, path: str):
        self.destinationPath = path
        self.logger = logging.getLogger("FileController")

    def saveFile(self, path: str, utilisateur: User):
        file = File(path)

        try:
            self.logger.debug("Save " + str(path) + "to" + self.destinationPath)
            destination = self.destinationPath + utilisateur.username + '/'
            FileEncryptor.encrypt(destination + os.path.basename(path), file, utilisateur)
            return True
        except Exception as saveFileError:
            self.logger.error(saveFileError)
            return False

    def getFile(self, path: str, utilisateur: User):
        file = File(self.destinationPath + utilisateur.username + "/" + path)
        try:
            FileEncryptor.decrypt(self.destinationPath + utilisateur.username + "/" + path, file, utilisateur)
            return True
        except Exception as saveFileError:
            self.logger.error(saveFileError)
            return False

