# EXTERNAL CLASS SKELETONS
from os.path import basename
class User:
    def __init__(self):
        # TODO: set generated values related to user here
        # hashpwd => b"My password is awesome"
        self.infos = {"username": "Toto", "hashpwd": b"&P5\xc2t\xcaU\xa4\xaa\xf0>M5\x99\xc2\x15ro\xdf\t\xf4\x03<L\xb5\x82\x9bK\xdf\xd6\xa2v"}

class File:
    def __init__(self, pathToFile):
        # TODO: set generated values related to file here
        self.infos = {"filename": basename(pathToFile)}
        self._path = pathToFile

    def openStream(self, readWriteMode):
        return open(self._path, readWriteMode)