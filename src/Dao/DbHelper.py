import sqlite3

class DbHelper:

    connection = None
    cursor = None

    def __init__(self):
        self.connection = sqlite3.connect('./databases/users.sqlite')
        self.cursor = self.connection.cursor()

    def query(self,query,param):
        self.cursor.execute(query,param)

    def getFirstResult(self):
        return self.cursor.fetchone()

    def close(self):
        self.connection.close()