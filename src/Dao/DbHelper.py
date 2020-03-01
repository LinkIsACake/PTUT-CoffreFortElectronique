import sqlite3

class DbHelper:

    connection = None
    cursor = None

    def __init__(self, path:str):
        try:
            self.connection = sqlite3.connect(path)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print("An error has occured while opening the database:", e.args[0])

    def query(self,query,param):
        self.cursor.execute(query,param)

    def getFirstResult(self):
        return self.cursor.fetchone()

    def close(self):
        self.connection.close()