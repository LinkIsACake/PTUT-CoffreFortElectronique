from nacl import secret, utils

from EncryptCore.beforeImplemented import * # TODO: change this import to User and File objects when implemented
from EncryptCore.exceptions import EncryptionKeyError, CryptoError
from EncryptCore.Utilities import *

from hashlib import sha256
from random import randrange

"""
NOTE:
Les commentaires sont dépassés, ils seront modifiés d'ici peu.

"""


def encrypt(destination: str, file: File, user: User):
    """
    Encrypt a file content using its datas and the user datas
    :param destination: a path of the destination to the encrypted file
    :param file: a file object containing file infos
    :param user: a user object containing user infos
    """
    # Get the cryptoMod as random integer of a million [1M; 10M[
    cryptoMod = randrange(10**6, 10**7-1)
    # Create the encryption key using file infos, user infos and cryptoMod
    tmpKey = generateKey(file.infos, user.infos)
    # Compute a eTime as a value to store in file for retreiving cryptoMod
    bytesNeeded, cipherMod = generateCipherMod(tmpKey, cryptoMod)

    key = sha256(str(tmpKey % cryptoMod).encode())
    box = secret.SecretBox(key.digest())
    nonce = utils.random(secret.SecretBox.NONCE_SIZE)

    readStream = file.openStream("rb")
    writeStream = File(destination).openStream("wb")

    # Write a 48 bytes of crypted time chunk
    writeStream.write(bytesNeeded.to_bytes(2, 'big'))
    writeStream.write(cipherMod)

    # crypt the file
    try:
        finished = False
        while not finished:
            chunk = readStream.read(1024)
            if len(chunk) == 0: finished = True
            else: writeStream.write(box.encrypt(chunk, nonce))
    except CryptoError:
        raise EncryptionKeyError()
    finally:
        readStream.close()
        writeStream.close()

def decrypt(destination: str, file: File, user: User):
    """
    Decrypt a file content using its datas and the user datas
    :param destination: a path of the destination to the decrypted file
    :param file: a file object containt file infos
    :param user: a user object containing user infos
    """
    readStream = file.openStream("rb")
    # Read the crypted time chunk
    cipherModLength = int.from_bytes(readStream.read(2), 'big')
    cipherMod = int.from_bytes(readStream.read(cipherModLength), 'big')

    tmpKey = generateKey(file.infos, user.infos)
    cryptoMod = getModFromCipher(tmpKey, cipherMod)

    # Create the key using file infos, user infos and encryping time
    key = sha256(str(tmpKey % cryptoMod).encode())
    box = secret.SecretBox(key.digest())

    writeStream = File(destination).openStream("wb")

    try:
        finished = False
        while not finished:
            chunk = readStream.read(1024)
            if len(chunk) == 0: finished = True
            else: writeStream.write(box.decrypt(chunk))
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

