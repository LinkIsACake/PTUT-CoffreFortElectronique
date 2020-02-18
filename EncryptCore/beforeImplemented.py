from EncryptCore.exceptions import EncryptionKeyError, CryptoError

# EXTERNAL CLASS SKELETONS
class User:
    def __init__(self):
        # TODO: set generated values related to user here
        self.infos = {"userDataKey": "unecléspécialisépourlutilisateur"}

class File:
    def __init__(self, pathToFile):
        # TODO: set generated values related to file here
        self.infos = {"fileDataKey": "unecléspécialisépourlefichier"}

        self.__path = pathToFile

    def EncryptDecriptFile(self, destination, cryptographicFunction, nonce=None):
        readStream = open(self.__path, "rb")
        writeStream = open(destination, "wb")

        if nonce is None: cryptoFunc = lambda chunk: cryptographicFunction(chunk)
        else:             cryptoFunc = lambda chunk: cryptographicFunction(chunk, nonce)

        try:
            finished = False
            while not finished:
                chunk = readStream.read(1024)
                if len(chunk) == 0:  finished = True
                else: writeStream.write(cryptoFunc(chunk))
        except CryptoError:
            raise EncryptionKeyError()

        readStream.close()
        writeStream.close()