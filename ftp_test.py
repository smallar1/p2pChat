import ftplib
# def ftp_server():
#     ftp_cred = {
#         'HOSTNAME': "ftp.dlptest.com",
#         'USERNAME': "dlpuser",
#         'PASSWORD': "rNrKYTX9g7z3RgJRmxWuGHbeu",
#     }
#
#     server = ftplib.FTP(ftp_cred['HOSTNAME'], ftp_cred['USERNAME'], ftp_cred['PASSWORD'])
#     if server is None:
#         raise Exception('>Error creating FTP server')
#     server.encoding = 'utf-8'
#     return server


if __name__ == 'main':
    ftp_cred = {
        'HOSTNAME': "ftp.dlptest.com",
        'USERNAME': "dlpuser",
        'PASSWORD': "rNrKYTX9g7z3RgJRmxWuGHbeu",
    }

    ftpserver = ftplib.FTP(ftp_cred['HOSTNAME'], ftp_cred['USERNAME'], ftp_cred['PASSWORD'])

    ftpserver.encoding = 'utf-8'

    file = 'fart.txt'

    with open(file, 'rb') as f:
        # Command for Uploading the file "STOR filename"
        ftpserver.storbinary(f'STOR {file}', f)

    ftpserver.dir()

    file = 'new_fart.txt'

    with open(file, 'wb') as f:
        # Command for Uploading the file "STOR filename"
        ftpserver.retrbinary(f'RETR {file}', f.write)

    file = open(file, "r")
    print('File Content:', file.read())

    ftpserver.quit()
