from hashlib import sha256
from nacl import secret, utils
from time import time

from EncryptCore.beforeImplemented import *
from EncryptCore.exceptions import EncryptionKeyError, CryptoError
from EncryptCore.tools import reduce

# sha256(b"This key musy be keept secret in any circumstances !")
GLOBAL_TIME_ENC_KEY = b"2\x98\xc5$\xc2t\x92\x8b^\x033\xd9\xe0>\x95\xceja+J:\xf3RX~\x04\xf6k\xd3O\x10\xf4"

def generateKey(fileData, userData, ctime):
    """
    Generate a key from file datas and user datas
    :param fileData: a dictionary containing all file datas used to crypt a file (need to be unchanged through crypto! )
    :param userData: a dictionary containing all user datas used to crypt a file
    :param ctime: the current time in integer (since 1/1/1970)
    :return: 32 bytes key
    """

    # create a epsilon single digit number from a fixed data (might be mac ?)
    epsilon = reduce(ctime)
    string = str(ctime)
    for k,v in fileData.items(): string += "%s:%s" % (k,v)
    for k,v in userData.items(): string += "%s:%s" % (k,v)

    # sum all chars of string with a epsilon digit (0-9)
    pwd = b"".join([bytes([(ord(c) + epsilon) % 256]) for c in string])

    sha = sha256(pwd)
    return sha.digest()

def cryptTimeChunk(cTime):
    """
    Create a encrypted time byte string from current time using the GLOBAL_TIME_ENC_KEY
    :return: the current time in integer along with the bytes string containing an encrypted time
    """

    box = secret.SecretBox(GLOBAL_TIME_ENC_KEY)
    nonce = utils.random(secret.SecretBox.NONCE_SIZE)

    encTime = box.encrypt(cTime.to_bytes(8, 'big'), nonce)

    return encTime

def decryptTimeChunk(encTime):
    """
    Decrypt a crypted time chunk using the GLOBAL_TIME_ENC_KEY
    :return: a bytes string containing the time chunk
    """
    box = secret.SecretBox(GLOBAL_TIME_ENC_KEY)
    return box.decrypt(encTime)

def encrypt(destination, file, user):
    """
    Encrypt a file content using its datas and the user datas
    :param destination: a path of the destination to the encrypted file
    :param file: a file object containing file infos
    :param user: a user object containing user infos
    """
    # Get the current time as an integer
    cTime = int(time() * 10 ** 7)
    # Encrypt the time using the cryptTimeChunk method
    encTime = cryptTimeChunk(cTime)

    # Create the encryption key using file infos, user infos and current time
    key = generateKey(file.infos, user.infos, cTime)
    box = secret.SecretBox(key)
    nonce = utils.random(secret.SecretBox.NONCE_SIZE)

    readStream = file.openStream("rb")
    writeStream = File(destination).openStream("wb")

    """
    TODO: remove this chunk of code when it is proved that encTime length will stay fix
    timeLength = len(encTime)
    writeStream.write(timeLength.to_bytes(1, 'big'))
    """
    # Write a 48 bytes of crypted time chunk
    writeStream.write(encTime)

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
    """
    TODO: remove this chunk of code when it is proved that encTime length will stay fix
    timeLength = int.from_bytes(readStream.read(1), 'big')
    """
    # Read the crypted time chunk
    encTime = readStream.read(48)
    # Decrypt the time using the decryptTimeChunk method
    time = int.from_bytes(decryptTimeChunk(encTime), 'big')

    # Create the key using file infos, user infos and encryping time
    key = generateKey(file.infos, user.infos, time)
    box = secret.SecretBox(key)

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

