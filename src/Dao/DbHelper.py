import sqlite3
import os


class DbHelper:
    connection = None
    cursor = None

    def __init__(self, path: str):
        if not self.check_file(path):
            open('path', 'w+').close()

        try:
            self.connection = sqlite3.connect(path)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print("An error has occured while opening the database:", e.args[0])

    @staticmethod
    def check_file(path: str):
        return os.path.isfile(path)

    def query(self, query, param):
        self.cursor.execute(query, param)

    def getFirstResult(self) -> []:
        return self.cursor.fetchone()

    def queryAll(self, query, param) -> []:
        self.cursor.execute(query, param)
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()
