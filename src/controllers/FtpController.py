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
            self.ftpSession = FTP(url, login, password)

        print(self.ftpSession)

        self.ftpSession.login()

    def get_directory(self):
        self.logger.debug("getDirectory")
        current_directory = self.ftpSession.pwd()
        return current_directory

    def set_directory(self, newDir: str):
        self.logger.debug("setDirectory")

        try:
            self.ftpSession.cwd(newDir)
        except ftplib.error_perm as resp:
            if str(resp) == '550 Path does not exist':
                self.logger.error("550 Path does not exist")
                return False
            else:
                raise
        except Exception as ftpError:
            self.logger.error(ftpError)
        self.startPoint = newDir

    def upload_file(self, pathToSend: str):
        self.logger.debug("uploadFile")
        try:
            with open(pathToSend, 'wb') as fileToSend:
                self.ftpSession.storbinary('STOR ' + pathToSend, fileToSend)
        except Exception as err:
            self.logger.error(err)

    def notify(self, **kwargs):
        pass

    def list_directory(self) -> bool:
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

    def quit_session(self):
        self.ftpSession.close()
