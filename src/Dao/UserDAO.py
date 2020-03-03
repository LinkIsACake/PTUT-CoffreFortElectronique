from .DAO import DAO
import sqlite3
import os
from nacl import pwhash
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
        self.database.query("SELECT * FROM Users WHERE username = ?", [username])
        result = self.database.getFirstResult()
        if not result:
            return result
        else:
            return False

    def createUser(self, username: str, password: str):
        try:

            hash_password = pwhash.str(password.encode())

            self.database.query("INSERT INTO Users VALUES (?,?)", [username, hash_password])
            self.database.connection.commit()
            return True
        except sqlite3.Error as e:
            print("An error has occured:", e.args[0])
            return False

    def checkCredentials(self, username: str, password: str) -> bool:
        self.database.query("SELECT * FROM Users WHERE username = ?", [username])
        result = self.database.getFirstResult()
        if len(result > 0):
            return pwhash.verify(result[1], password)
        else:
            return False
