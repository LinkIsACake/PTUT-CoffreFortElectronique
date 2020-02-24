from math import ceil

def generateKey(fileData: dict, userData: dict):
    """
    Generate a key from file datas and user datas
    :param fileData: a dictionary containing all file datas used to crypt a file (need to be unchanged through crypto! )
    :param userData: a dictionary containing all user datas used to crypt a file
    :return: a integer key
    """
    pwd = ""
    for k,v in fileData.items(): pwd += "%s:%s" % (k,v)
    for k,v in userData.items(): pwd += "%s:%s" % (k,v)

    return int.from_bytes(pwd.encode(), 'big')

def generateCipherMod(key: int, cryptoMod: int):
    """
    Create a cipher time from key and the cryptoTime using modulus algebra
    a % n = b
    (a - b) / n = k
    (a - b) / k = n
    Where:
    - a represents the key
    - n represents the time
    - b represents the remainder of a/n
    - k the quotient of the equation (cipher time)

    :param key: a integer key
    :param cryptoMod: a integer form time
    :return: the cipher of the time using the modulus algebra
    """
    b = key % cryptoMod
    cipherMod = (key - b) // cryptoMod

    # 2.418 result of tests. Don't know yet where does this number come from...
    bytesNeeded = ceil(len(str(cipherMod)) / 2.418) + 1
    cipherModBytes = cipherMod.to_bytes(bytesNeeded, 'big', signed=False)

    return bytesNeeded, cipherModBytes

def getModFromCipher(key: int, cipherMod: int):
    """
    Get the time of the cryptage from a cipher time
    :param key: the key to encrypt the file
    :param cipherMod: a cipher of the encryptage time
    :return: the time of the cryptage of the file
    """
    cryptoMod  = key // cipherMod
    return cryptoMod
