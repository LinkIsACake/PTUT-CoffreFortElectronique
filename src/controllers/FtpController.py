import ftplib
from ftplib import FTP
from src.Utils.Logger import Logger


class FtpController(Logger):
    url: str
    login: str
    password: str
    ftpSession: FTP
    directory: str
    dir: str

    def __init__(self, url: str, login: str = "anonymous", password: str = ""):
        Logger.__init__(self)

        self.url = url
        self.login = login
        self.password = password

        self.ftpSession = FTP(url, login, password)
        self.ftpSession.login()

    def getDirectory(self):
        self.logger.debug("getDirectory")

        self.dir = self.ftpSession.pwd()
        return self.dir

    def setDirectory(self, newDir: str):
        self.logger.debug("setDirectory")

        try:
            self.ftpSession.cwd(newDir)
        except ftplib.error_perm as resp:
            if str(resp) == '550 Path does not exist':
                return False
            else:
                raise
        self.directory = newDir

    def uploadFile(self, pathToSend: str):
        self.logger.debug("uploadFile")

        with open(pathToSend, 'wb') as fileToSend:
            self.ftpSession.storbinary('STOR ' + pathToSend, fileToSend)

    def listDirectory(self) -> bool:
        self.logger.debug("listDirectory")

        files = []
        try:
            files = self.ftpSession.nlst(self.directory)
            return files
        except ftplib.error_perm as resp:
            if str(resp) == '550 No files found':
                self.logger.error('550 No files found')
                return False
            else:
                raise

    def quitSession(self):
        self.ftpSession.close()
