from UserDAO import UserDAO

dao = UserDAO()
dao.createUser("andrethegiant","password2")
dao.createUser("josephjoestarthotslayer","NIGERUNDAYOOOOOO")

print(dao.checkCredentials("andrethegiant","password2"))
print(dao.checkCredentials("andrethegiant","password3"))

dao.close()