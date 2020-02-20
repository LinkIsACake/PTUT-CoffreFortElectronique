from src.DAO import DAO
import sqlite3

class UserDAO(DAO):
    database = None
    
    def __init__(self):
        DAO.__init__(self)

    def close(self):
        DAO.close(self)

    def fetchUser(self, username):
        self.database.query("SELECT * FROM Users WHERE username = ?", [username])
        result = self.database.getFirstResult()
        if result != None:
            return result
        else:
            return False

    def createUser(self, username, password):
        try:
            self.database.query("INSERT INTO Users VALUES (?,?)", [username,password])
            self.database.connection.commit()
            return True
        except sqlite3.Error as e:
            print("An error has occured:", e.args[0])
            return False

    def checkCredentials(self,username,password):
        self.database.query("SELECT * FROM Users WHERE username = ? AND password = ?", [username, password])
        result = self.database.getFirstResult()
        return (result != None)
