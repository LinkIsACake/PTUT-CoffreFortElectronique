import base64

from nacl import secret, utils
from hashlib import sha256
from random import randrange

from nacl.public import SealedBox

from .exceptions import EncryptionKeyError, CryptoError

import sys

from .Utilities import generateKey, generateCipherMod, unbundleSizeAndRest, getModFromCipher

sys.path.append('..')

from models.User import User
from models.File import File
import pickle

def encrypt(destination: str, file: File, user: User):
    """
    Encrypt a File object and place it to it's destination path

    :param destination: a destination path
    :param file: the File object to encrypt and that store all file related infos
    :param user: the User object that store all user related infos
    """

    # Create a random number that will be used as a base to modify the generated key
    base = randrange(10 ** 6, 10 ** 7 - 1)

    # Create the temporary key from the files and user infos
    tmpKey = generateKey(file.infos, user.infos)
    # Create a cipher of the base for being saved in the file (see Utilities:generateCipherMod for more details)
    sizeAndRest, cipherBase = generateCipherMod(tmpKey, base)

    test = unbundleSizeAndRest(int.from_bytes(sizeAndRest, "little"))

    # Create a sha256 hash of the temporary key on the random base and create the crypto box from it
    key = sha256(str(tmpKey % base).encode())
    box = secret.SecretBox(key.digest())
    nonce = utils.random(secret.SecretBox.NONCE_SIZE)

    # open the input file (decrypted) and the output file (encrypted)
    readStream = file.openStream("rb")
    writeStream = File(destination).openStream("wb")

    # write the length of the cipher base and the base of the key
    writeStream.write(sizeAndRest)
    writeStream.write(cipherBase)

    # Read every 1024 bytes of the input file, encrypt it and save it to the output file
    try:
        finished = False
        while not finished:
            chunk = readStream.read(65536)
            if len(chunk) == 0:
                finished = True
            else:
                writeStream.write(box.encrypt(chunk, nonce))
    except CryptoError:
        raise EncryptionKeyError()
    finally:
        readStream.close()
        writeStream.close()


def decrypt(destination: str, file: File, user: User):
    """
    Decrypt a file and place it on it's destination path

    :param destination: the destination path of the decrypted file
    :param file: the encrypted file and all it's informations needed to generate the key
    :param user: the user that contains all the infos used to generate the key
    """

    # open the input file (encrypted)
    readStream = file.openStream("rb")

    # get the length and rest bundle of the cipher base saved in the file and get the cipher base
    sizeAndRestBundle = int.from_bytes(readStream.read(4), 'little')
    size, rest = unbundleSizeAndRest(sizeAndRestBundle)
    cipherBase = int.from_bytes(readStream.read(size), 'big')

    # generate the key using the file infos and the user infos
    tmpKey = generateKey(file.infos, user.infos)

    # generate the base using the temporary key and the cipher base from the file (see Utilities:getModFromCipher)
    base = getModFromCipher(tmpKey, cipherBase, rest)

    # create the sha256 hash from the temporary key on the base recovered and create the crypto box from it
    key = sha256(str(tmpKey % base).encode())
    box = secret.SecretBox(key.digest())

    # open the output file (decrypted)
    writeStream = File(destination).openStream("wb")

    # read every 1024 bytes of the file and decrypt it using the box
    try:
        finished = False
        while not finished:
            chunk = readStream.read(65536 + 40)
            if len(chunk) == 0:
                finished = True
            else:
                writeStream.write(box.decrypt(chunk))
    except CryptoError:
        raise EncryptionKeyError()
    finally:
        readStream.close()
        writeStream.close()

if __name__ == '__main__':
    print("Tests of EncryptCore:FileEncryptor")

    dec = File("./tests/test.txt")
    encrypt("./tests/encFolder/test.txt", dec, User())

    enc = File("./tests/encFolder/test.txt")
    decrypt("./tests/decFolder/test.txt", enc, User())
