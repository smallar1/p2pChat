import socket
import re
import sys

our_socket = socket.socket()

HOST = ''
PORT = 8080

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
                    msg = connfd.recv(1024)
                    if msg:
                        connfd.sendall(msg)

                        # handle close request
                        if str(msg)[2:-1] == 'close server':
                            print(f">Closing Server...")
                            closing = True
                            break

                        #handle disconnect request
                        if str(msg)[2:-1] == 'disconnect':
                            print(f">{client_address[0]} disconnected")
                            connfd.close()
                            break

                        #message sent
                        print(f"{client_address[0]}: {str(msg)[2:-1]}\nbytes: {len(msg)}")
                except:
                    continue