import sqlite3

databaseConnection = sqlite3.connect('./databases/users.sqlite')
db = databaseConnection.cursor()

def fetchUser(username):
    db.execute("SELECT * FROM Users WHERE Username = ?", [username])
    result = db.fetchone()
    if result != None:
        return result
    else:
        return False

def createUser(username,password):
    try:
        db.execute("INSERT INTO Users VALUES (?,?)",[username,password])
        databaseConnection.commit()
        return True
    except sqlite3.Error as e:
        print("An error occurred:", e.args[0])
        return False

print(createUser("andre","thegiant"))

databaseConnection.close()