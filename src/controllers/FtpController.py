from ftplib import import FTP

sys.path.append('..')

class FtpController:
    
    url:str
    login:str
    password:str
    ftpSession:str
    directory:str

    def __init__(self,url,login:str="anonymous",password:str=""):
        self.url = url
        self.login = login
        self.password = password

        ftpSession = FTP(url,login,password)
        ftpSession.login()

    def getDirectory(self):
        self.dir = self.ftpSession.pwd()
        return self.dir

    def setDirectory(self,newDir:str):
        try:
            self.ftpSession.cwd(newDir)
        except ftplib.error_perm, resp:
            if str(resp) == '550 Path does not exist':
                return False
            else:
                raise
        self.directory = newDir
    
    def uploadFile(self,pathToSend:str):
        with open(pathToSend, 'wb') as fp:
            ftp.storbinary('STOR '+pathToSend, fp)

    def listDirectory(self):
        files = []
        try:
            files = ftp.nlst(self.directory)
            return files
        except ftplib.error_perm, resp:
            if str(resp) == '550 No files found':
                return False
            else:
                raise
        
    def quitSession(self):
        self.ftpSession.close()

