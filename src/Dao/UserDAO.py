from .DAO import DAO
import sqlite3

class UserDAO(DAO):
    database = None
    
    def __init__(self, path:str="../databases/users.sqlite"):
        DAO.__init__(self,path)

    def close(self):
        DAO.close(self)

    def fetchUser(self, username:str):
        self.database.query("SELECT * FROM Users WHERE username = ?", [username])
        result = self.database.getFirstResult()
        if result != None:
            return result
        else:
            return False

    def createUser(self, username:str, password:str):
        try:
            self.database.query("INSERT INTO Users VALUES (?,?)", [username,password])
            self.database.connection.commit()
            return True
        except sqlite3.Error as e:
            print("An error has occured:", e.args[0])
            return False

    def checkCredentials(self, username:str, password:str):
        self.database.query("SELECT * FROM Users WHERE username = ? AND password = ?", [username, password])
        result = self.database.getFirstResult()
        return (result != None)
