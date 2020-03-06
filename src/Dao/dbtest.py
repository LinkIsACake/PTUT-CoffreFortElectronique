from src.Dao.UserDAO import UserDAO

dao = UserDAO()
dao.createUser("andrethegiant","password2")
dao.createUser("joseph","testpassword")

print(dao.checkCredentials("andrethegiant","password2"))
print(dao.checkCredentials("andrethegiant","password3"))

dao.close()
