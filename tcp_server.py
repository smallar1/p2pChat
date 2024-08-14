import socket
from enum import Enum
import re
import sys

# define macros
class reproto(Enum):
    PUT = 'PUT ([\w\.]*) (.*)',
    GET = 'GET ([\w\.]*)',


#define code_200 "OK"
#define code_201 "Created"
#define code_400 "Bad Request"
#define code_403 "Forbidden"
#define code_404 "Not Found"
#define code_500 "Internal Server Error"
#define code_501 "Not Implemented"
#define code_505 "Version Not Supported"
def handle_response(code, connfd):
    if code == 200:
        pass
    elif code == 201:
        pass
    elif code == 400:
        pass
    elif code == 403:
        pass
    elif code == 404:
        pass
    elif code == 500:
        pass
    elif code == 501:
        pass
    elif code == 505:
        pass


our_socket = socket.socket()

HOST = ''
PORT = int(sys.argv[1])

LIST_OF_USERS = []

closing = False



# bind a socket and listen
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    # keep server running and waiting to accept connections
    while 1:
        if closing:
            break

        connfd, client_address = s.accept()

        with connfd:
            print(f">New connection by {client_address[0]}")
            LIST_OF_USERS.append(client_address)

            # allow a user to stay connected without disconnecting between messages
            while 1:
                try:
                    # TODO handle 1024 cutoff
                    msg = connfd.recv(1024)
                    if msg:

                        #connfd.sendall(msg)

                        # stringized version of msg
                        msg = str(msg)[2:-1]

                        # handle close request
                        if msg == 'close server':
                            print(f">Closing Server...")
                            closing = True
                            break

                        # handle disconnect request
                        if msg == 'disconnect':
                            print(f">{client_address[0]} disconnected")
                            connfd.close()
                            break

                        # message sent
                        # TODO: change bytes to file body, whether it was put or grabbed.
                        print(f"{client_address[0]}: {msg}\nbytes: {len(msg) + 3}")

                        # handle get/put
                        puts_obj = re.fullmatch(''.join(reproto.PUT.value), msg)

                        gets_obj = re.fullmatch(''.join(reproto.GET.value), msg)

                        if puts_obj is not None:
                            try:
                                with open (f"io_server_files/{puts_obj[1]}", 'w') as f:
                                    f.write(puts_obj[2])
                                    print('file written') # debug for putting file
                                    connfd.sendall(bytes("200: File Written", "utf-8")) # debug for putting file
                            except PermissionError:
                                print("error opening file") # debug if file cannot be put
                                connfd.sendall(bytes("403: Permission Denied", "utf-8"))
                            puts_obj = None

                        elif gets_obj is not None:
                            try:
                                with open(f'io_server_files/{gets_obj[1]}') as f:
                                    file_contents = bytes(f.read(), 'utf-8')
                                    connfd.sendall(file_contents)
                            except IOError:
                                connfd.sendall(bytes("404: file not found", 'utf-8'))
                            gets_obj = None
                        else:
                            print("uh oh")


                except Exception:
                    continue