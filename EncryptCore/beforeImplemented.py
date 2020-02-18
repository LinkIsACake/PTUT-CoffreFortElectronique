# EXTERNAL CLASS SKELETONS
class User:
    def __init__(self):
        # TODO: set generated values related to user here
        self.infos = {"userDataKey": "unecléspécialisépourlutilisateur"}

class File:
    def __init__(self, pathToFile):
        # TODO: set generated values related to file here
        self.infos = {"fileDataKey": "unecléspécialisépourlefichier"}
        self._path = pathToFile

    def openStream(self, readWriteMode):
        return open(self._path, readWriteMode)