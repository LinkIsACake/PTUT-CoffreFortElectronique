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

    def __init__(self, path:str):
        self.destinationPath = path
        self.logger = logging.getLogger("FileController")


    def saveFile(self, path: str, utilisateur: User):
        file = File(path)
        
        try:
            FileEncryptor.encrypt(self.destinationPath, file, utilisateur)
            return True
        except Exception as saveFileError:
            self.logger.error(saveFileError)
            return False


    def getFile(self, path: str, utilisateur: User):
        file = File(path)

        try:
            FileEncryptor.decrypt(self.destinationPath, file, utilisateur)
            return True
        except Exception as saveFileError:
            self.logger.error(saveFileError)
            return False        


if __name__ == '__main__':
    print("Test fichier et utilisateur")

    #dec = File("../Files/test.txt")
    controller = FileController("../Files")
    controller.saveFile("../Files/test.txt",User())