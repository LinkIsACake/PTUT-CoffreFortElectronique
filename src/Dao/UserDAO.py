import sqlite3
import nacl.pwhash
import nacl.exceptions

from .DAO import DAO


class UserDAO(DAO):
    database = None
    databaseCreationScript = 'CREATE TABLE "Users" ("username"	TEXT NOT NULL, "password" TEXT NOT NULL, PRIMARY KEY("username"));'

    # Initialisation du DAO et création de la table users si elle n'existe pas
    def __init__(self, path: str = "ressource/users.sqlite"):
        DAO.__init__(self, path)
        if not self.init:
            self.database.query(self.databaseCreationScript, [])

    # Fermeture de la connexion
    def close(self):
        DAO.close(self)

    def userExist(self,username:str):
        """
        Rechercher un utilisateur dans la table users à partir de son nom
        d'utilisateur et retour vrai si le trouve, faux sinon

        :param username: nom d'utilisateur à rechercher dans la base
        """
        self.logger.debug("fetchUser")
        self.database.query("SELECT * FROM Users WHERE username = ?", [username])
        result = self.database.getFirstResult()
        if result:
            return True
        else:
            return False

    def fetchUser(self, username: str):
        """
        Rechercher un utilisateur dans la table users à partir de son nom
        d'utilisateur et le retourner

        :param username: nom d'utilisateur à rechercher dans la base
        """
        self.logger.debug("fetchUser")
        self.database.query("SELECT * FROM Users WHERE username = ?", [username])
        result = self.database.getFirstResult()
        if not result:
            return result
        else:
            return False

    def createUser(self, username: str, password: str) -> bool:
        """
        Insertion d'un nouvel utilisateur dans la table users sans oublier de
        hasher le mot-de-passe.

        :param username: nom d'utilisateur à insérer
        :param password: mot-de-passe à hasher puis insérer dans la table

        :return Retourne True si aucune erreur n'a été détecté
                Retourne False si l'insertion échoue.
        """

        self.logger.debug("createUser")
        try:

            self.database.query("INSERT INTO Users VALUES (?,?)", [username, password])
            self.database.connection.commit()
            return True
        except sqlite3.Error as e:
            print("An error has occured:", e.args[0])
            return False

    def checkCredentials(self, username: str, password: str) -> bool:
        """
        Vérifie que le couple username/password correspond bien à un utilisateur
        présent dans la table users.

        :param utilisateur: nom d'utilisateur à vérifier
        :param password: mod-de-passe à vérifier
        """


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
                type(password)
                nacl.pwhash.verify(hash_password, password.encode())
            except nacl.pwhash.InvalidkeyError as err:
                return False
            except Exception as pwhashError:
                self.logger.error(pwhashError)
                return False

            self.logger.debug("password is verified")
            return True
        else:
            self.logger.debug("user not found")
            return False

    def fetchAllUsers(self)->[]:
        """
        Retourne tous les noms d'utilisateurs sous la forme d'un tableau de strings.

        :return Retourne un tableau de noms d'utilisateurs si la requête fonctionne
                Retourne False si la requête échoue.
        """
        try:
            rows = self.database.queryAll("SELECT username FROM Users",[])
            return [row[0] for row in rows]
        except sqlite3.Error as e:
            print("An error has occured:",e.args[0])
            return False