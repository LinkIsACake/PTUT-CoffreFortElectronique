from hashlib import sha256
from nacl import secret, utils

from EncryptCore.beforeImplemented import *
from EncryptCore.tools import reduce

def generateKey(fileData, userData):
    """
    Generate a key from file datas and user datas
    :param fileData: a dictionary containing all file datas used to crypt a file (need to be unchanged through crypto! )
    :param userData: a dictionary containing all user datas used to crypt a file
    :return: 32 bytes key
    """

    # create a epsilon single digit number from a fixed data (might be mac ?)
    epsilon = reduce(42) # TODO: change this line to a no-fixed value
    string = "{fileDataKey}{userDataKey}".format(**fileData, **userData)

    # sum all chars of string with a epsilon digit (0-9)
    pwd = b"".join([bytes([(ord(c) + epsilon) % 256]) for c in string])

    sha = sha256()
    sha.update(pwd)
    return sha.digest()

def encrypt(destination, file, user):
    """
    Encrypt a file content using its datas and the user datas
    :param destination: a path of the destination to the encrypted file
    :param file: a file object containing file infos and a filestream
    :param user: a user object containing user infos
    """
    key = generateKey(file.infos, user.infos)
    box = secret.SecretBox(key)
    nonce = utils.random(secret.SecretBox.NONCE_SIZE)

    file.EncryptDecriptFile(destination, box.encrypt, nonce)

def decrypt(destination, file, user):
    """
    Decrypt a file content using its datas and the user datas
    :param destination: a path of the destination to the decrypted file
    :param file: a file object containt file infos and a filestream
    :param user: a user object containing user infos
    """
    key = generateKey(file.infos, user.infos)
    box = secret.SecretBox(key)
    file.EncryptDecriptFile(destination, box.decrypt)

if __name__ == '__main__':
    dec = File("./tests/test.txt")
    encrypt("./tests/encTest.txt", dec, User())

    enc = File("./tests/encTest.txt")
    decrypt("./tests/decTest.txt", enc, User())

