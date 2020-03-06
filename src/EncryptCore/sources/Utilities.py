from math import log, ceil

def bundleSizeAndRest(size: int, rest: int):
    """
    # get a bundled number of the rest and the bytes needed to store the cipher
    # Note: some arbitrary modification is done to this number to protect it against reverse engineering

    :param size: the size of the cipher to bundle (max: 255)
    :param rest: the rest of the cipher to bundle (max: 16 777 215)
    :return: a bundled number containing the size and the rest of the cipher
    """
    if size > 255 or rest > 16777215:
        raise ValueError("The numbers are too big to be bundled together... (size: %d, rest: %d)" % (size, rest))

    # get the 2nd byte of the rest and shift it to the topmost position
    swapValue = (rest & 0x0000ff00) << 16
    # shift the value of the bytesNeeded to the 3rd position
    size <<= 8
    # create the bundled value with this memory sheme:  rest_1|rest_2|bytesNeeded|rest_0
    sizeAndRestBundle = (rest & 0x00ff00ff) | size | swapValue

    # change the endianess of the number and return the result
    return sizeAndRestBundle.to_bytes(4, 'little')

def unbundleSizeAndRest(sizeAndRestBundle: int):
    """
    Get the size and the rest of the cipher base from a bundled integer

    :param sizeAndRestBundle: a bundled number containing the size and the rest of the cipher
    :return: the size and the rest as a tuple
    """
    if sizeAndRestBundle > 0xffffffff:
        raise ValueError("The bundled number is too big.")

    # get the size from the 2nb byte
    size = (sizeAndRestBundle & 0x0000ff00) >> 8
    # get the swap byte from the topmost byte
    swapValue = (sizeAndRestBundle & 0xff000000) >> 16
    # set the swap byte at the 2ns byte and clear the topmost byte
    rest = (sizeAndRestBundle & 0x00ff00ff) | swapValue

    return size, rest

def generateKey(fileData: dict, userData: dict):
    """
    Generate a key from file infos and user infos dictionaries

    :param fileData: a dictionary that contain all file infos used to create the key
    :param userData: a dictionary that contain all user infos used to create the key
    :return: a integer equavalent of all serialized values
    """

    # Serialize all file infos and user infos
    pwd = ""
    for k,v in fileData.items(): pwd += "%s:%s" % (k,v)
    for k,v in userData.items(): pwd += "%s:%s" % (k,v)

    # get the int equivalent of the bytes serialized infos in order to be used with a given base
    return int.from_bytes(pwd.encode(), 'big')

def generateCipherMod(key: int, base: int):
    """
    cipher a given base using a temporary key

    :param key: a temporary integer key
    :param base: a integer base
    :return: a cipher base along with a bundled size & rest integer

    given the relation:    a = k*b + r
    then:                  a-r = k*b
    and:                   b = (a-r)/k

    So let's say that k and r will be stored in the file, a is our key, b is the base
    So to cipher the base we will do:
    cipher = key // base
    rest   = key % base

    And to decipher the base we will do:
    base = (key-rest)//cipher
    """

    cipher = key // base
    rest = key % base

    # this need to be lower than 255
    bytesNeeded = ceil(log(cipher, 256))

    if bytesNeeded > 255:
        raise ValueError("The cipher of the base is larger than 255 bytes...")

    bundledSizeAndRest = bundleSizeAndRest(bytesNeeded, rest)

    cipherBytes = cipher.to_bytes(bytesNeeded, 'big', signed=False)

    return bundledSizeAndRest, cipherBytes

def getModFromCipher(key: int, cipher: int, rest: int):
    """
    get the base from the sipher, the key and the rest values

    :param key: a temporary integer key
    :param cipher: the ciphered base retreived from the file
    :param rest: the rest of the equation (see Utilities:generateCipher)
    :return: a integer base
    """
    base = (key-rest) // cipher
    return base
