from .DAO import DAO
import sqlite3
import os
from nacl import pwhash,exceptions
import logging

class UserDAO(DAO):
    database = None
    databaseCreationScript = 'CREATE TABLE "Users" ("username"	TEXT NOT NULL, "password" TEXT NOT NULL, PRIMARY KEY("username"));'

    def __init__(self, path: str = "../ressource/users.sqlite"):
        DAO.__init__(self, path)
        if not self.init:
            self.database.query(self.databaseCreationScript, [])

    def close(self):
        DAO.close(self)

    def fetchUser(self, username: str):
        self.logger.debug("fetchUser")
        self.database.query("SELECT * FROM Users WHERE username = ?", [username])
        result = self.database.getFirstResult()
        if not result:
            return result
        else:
            return False

    def createUser(self, username: str, password: str) -> bool:
        self.logger.debug("createUser")
        try:
            hash_password = pwhash.scrypt.str(password.encode('utf8'))

            self.database.query("INSERT INTO Users VALUES (?,?)", [username, hash_password])
            self.database.connection.commit()
            return True
        except sqlite3.Error as e:
            print("An error has occured:", e.args[0])
            return False

    def checkCredentials(self, username: str, password: str) -> bool:
        self.logger.debug("checkCredentials")

        try:
            self.database.query("SELECT * FROM Users WHERE username = ?", (username,))
        except Exception as err:
            self.logger.error(err)

        result = self.database.getFirstResult()
        if result:
            self.logger.debug("user found, check checkCredentials")

            try:
                hash_password = result[1]
                pwhash.verify(hash_password, password.encode())
            except exceptions.InvalidkeyError as err:
                return False
            except Exception as pwhashError:
                self.logger.error(pwhashError)
                return False

            self.logger.debug("password is verify")
            return True
        else:
            return False
