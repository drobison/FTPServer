mypath = '/home/cpsc473/Desktop/471/FtpServer/ServerFolder'

onlyfiles = [ f for f in listdir(ServerFolder) if isfile(join(ServerFolder,f)) ]
