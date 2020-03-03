from os.path import basename


class File:
    def __init__(self, pathToFile):
        # TODO: set generated values related to file here
        self.infos = {"filename": basename(pathToFile)}
        self._path = pathToFile

    def openStream(self, readWriteMode: str):
        return open(self._path, readWriteMode)