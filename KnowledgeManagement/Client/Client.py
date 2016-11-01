"""creates all the functions that a user can perform
   Client object gets instantiated and used in UserInterface.py"""

import socket
import json

class Client:

    # define connection
    def __init__(self):
        HOST = 'localhost'
        PORT = 8787
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((HOST,PORT))

    # login after connected to server
    def login(self, username, pword):
        packet = json.dumps({'username': username, 'pword': pword})
        self.sock.send(packet.encode())

        # receives response
        response = self.sock.recv(1024).decode()
        return response

    def upload(self,uF):
        #send filename
        s.send(uF.encode())
        #enter file category
        cat = str(input('Please enter a file category: '))
        s.send(cat.encode())
        #enter keywords
        keys = str(input('Please enter a list of keywords: '))
        s.send(keys.encode())
        
        #prepare file for transfer
        s.send("SOF".encode())
        f=open (uF, "rb")
        #break file down into 1024 byte chunks
        chunk = f.read(1024)
        #send file in 1024 byte chunks
        while (chunk):
            s.send(chunk)
            chunk = f.read(1024)
        ##s.send("EOF")
        #close connection
        s.close()
