from nacl.exceptions import CryptoError

class EncryptionKeyError(CryptoError):
    def __init__(self, *args):
        super().__init__(self, "The key seams to be unvaliable... "
                                 "Please check the informations used to generate it...", *args)