import os


from src.EncryptCore.sources import FileEncryptor

import logging
from src.models.File import File
from src.models.User import User

from src.Utils.Logger import Logger


class FileController(Logger):
    destinationPath: str

    def __init__(self, path: str):
        Logger.__init__(self)

        self.destinationPath = path

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
            FileEncryptor.decrypt(self.destinationPath + "/" + path, file, utilisateur)
            return True
        except Exception as saveFileError:
            self.logger.error(saveFileError)
            return False

