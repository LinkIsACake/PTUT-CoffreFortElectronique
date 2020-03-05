class User:

    def __init__(self, username: str, password: bytes):
        # TODO: set generated values related to user here
        # hashpwd => b"My password is awesome"
        self.username = username
        self.password = password
        self.infos = {
            "username": self.username,
            "hashpwd": self.password
        }
