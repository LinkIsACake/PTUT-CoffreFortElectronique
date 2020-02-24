from nacl.exceptions import CryptoError # imported in File

class EncryptionKeyError(Exception):
    def __init__(self, *args):
        Exception.__init__(self, "The key seams to be unvaliable... "
                                 "Please check the informations used to generate it...", *args)