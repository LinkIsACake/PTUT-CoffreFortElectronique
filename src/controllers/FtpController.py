import ftplib
from ftplib import FTP
from src.Utils.Logger import Logger


class FtpController(Logger):
    url: str
    login: str
    password: str
    ftpSession: FTP
    startPoint: str
    dir: str

    def __init__(self, url: str, login: str = None, password: str = None):
        Logger.__init__(self)

        self.url = url
        self.login = login
        self.password = password
        self.startPoint = "/"

        if not login:
            self.ftpSession = FTP(url)
        else:
            self.ftpSession = FTP(url, login,password)
        self.ftpSession.login()


    def getDirectory(self):
        self.logger.debug("getDirectory")
        current_directory = self.ftpSession.pwd()
        return current_directory

    def setDirectory(self, newDir: str):
        self.logger.debug("setDirectory")

        try:
            self.ftpSession.cwd(newDir)
        except ftplib.error_perm as resp:
            if str(resp) == '550 Path does not exist':
                return False
            else:
                raise
        self.startPoint = newDir

    def uploadFile(self, pathToSend: str):
        self.logger.debug("uploadFile")

        with open(pathToSend, 'wb') as fileToSend:
            self.ftpSession.storbinary('STOR ' + pathToSend, fileToSend)

    def notify(self, **kwargs):
        pass

    def listDirectory(self) -> bool:
        self.logger.debug("listDirectory")

        files = []
        try:
            files = self.ftpSession.nlst(self.startPoint)
            return files
        except ftplib.error_perm as resp:
            if str(resp) == '550 No files found':
                self.logger.error('550 No files found')
                return False
            else:
                raise

    def quitSession(self):
        self.ftpSession.close()
