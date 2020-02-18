def reduce(number):
    """
    Sum all digits to a number recurcivly untill le length of the number is 1
    :param number: a natural number
    :return: the number if it's size is 1, the sum of it's digits otherwise
    """
    if isinstance(number, int):
        string = str(number)
    elif isinstance(number, str) and number.isnumeric():
        string = number
    else:
        raise TypeError("The number need to be a string containing only digits or a integer")

    if len(string) == 1:
        return number
    else:
        new = sum([int(c) for c in string])
        return reduce(new)