
from nacl import secret, utils
from time import time

from EncryptCore.beforeImplemented import *
from EncryptCore.exceptions import EncryptionKeyError, CryptoError
from EncryptCore.Utilities import *

def encrypt(destination, file, user):
    """
    Encrypt a file content using its datas and the user datas
    :param destination: a path of the destination to the encrypted file
    :param file: a file object containing file infos
    :param user: a user object containing user infos
    """
    # Get the cryptoTime as an integer precise whose define the current time at it's 10 millionth precision
    cryptoTime = int(time() * 10 ** 7)
    # Create the encryption key using file infos, user infos and cryptoTime
    tmpKey = generateKey(file.infos, user.infos)
    # Compute a eTime as a value to store in file for retreiving cryptoTime
    bytesNeeded, cipherTime = generateCipherTime(tmpKey, cryptoTime)

    key = sha256(str(tmpKey % cryptoTime).encode())
    box = secret.SecretBox(key.digest())
    nonce = utils.random(secret.SecretBox.NONCE_SIZE)

    readStream = file.openStream("rb")
    writeStream = File(destination).openStream("wb")

    # Write a 48 bytes of crypted time chunk
    writeStream.write(bytesNeeded.to_bytes(2, 'big'))
    writeStream.write(cipherTime)

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

def decrypt(destination, file, user):
    """
    Decrypt a file content using its datas and the user datas
    :param destination: a path of the destination to the decrypted file
    :param file: a file object containt file infos
    :param user: a user object containing user infos
    """
    readStream = file.openStream("rb")
    # Read the crypted time chunk
    cipherTimeLength = int.from_bytes(readStream.read(2), 'big')
    cipherTime = int.from_bytes(readStream.read(cipherTimeLength), 'big')

    tmpKey = generateKey(file.infos, user.infos)
    cryptoTime = getTimeFromCipher(tmpKey, cipherTime)
    # Decrypt the time using the decryptTimeChunk method

    # Create the key using file infos, user infos and encryping time
    key = sha256(str(tmpKey % cryptoTime).encode())
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
    dec = File("./tests/test.txt")
    encrypt("./tests/encFolder/test.txt", dec, User())

    enc = File("./tests/encFolder/test.txt")
    decrypt("./tests/decFolder/test.txt", enc, User())

