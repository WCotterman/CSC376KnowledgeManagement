"""accepts incoming client connections, then assigns each client a data retriever"""

import sys
import socket
from Data_Retriever import DataRetriever

if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 8787

    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((HOST,PORT))
    print('server side')

    s.listen(10)
    while True:
        sock, address = s.accept()
        print (address) # display connected client
        DataRetriever(sock).start() #start communicating with the client
