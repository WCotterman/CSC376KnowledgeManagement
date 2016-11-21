"""All the functions that a user can perform.
   The client object gets instantiated and used in ui.py"""

import socket
import json
import time
import os,sys

class Client:

    def __init__(self):
        """
        Creates a socket for the client, connects to server
        """

        host = 'localhost'
        port = 8787
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect((host,port))

    def login(self, username, pword):
        """
        Logs the user in once connected to the server

        :param username: user's name
        :param pword: user's password

        :return: 0 if username doesn't exist or incorrect password OR
                 1 if username exists and enters correct password
        """

        # serialize the username and pword into json
        info = json.dumps({'type': 'login',
                           'username': username,
                           'pword': pword})

        self.sock.send(info.encode())

        # wait for response
        response = int(self.sock.recv(1024).decode())
        return response

    def register(self, username, pword):
        '''
        Registers a new user

        :param username: new user name
        :param pword: new user password (encrypyted)

        :return: 0 if username is not unique (can't have duplicate usernames)
                 1 if username is unique and user is put in db
        '''

        # serialize the username and pword into json
        info = json.dumps({'type': 'register',
                           'username': username,
                           'pword': pword})

        self.sock.send(info.encode())

        # wait for response
        response = int(self.sock.recv(1024).decode())
        return response

    def upload(self, fileName, category, keywords):
        """
        Asks the data_retriever to upload a file to the db

        :param fileName: name of new file (file is stored on user's computer)
        :param category: file category
        :param: keywords: file keywords

        :return: 0 if upload is not successful
                 1 if upload is successful

        """

        # initial msg
        info = json.dumps({'type': 'upload',
                           'user': self.name,
                           'name': fileName,
                           'category': category,
                           'keywords': keywords})

        self.sock.send(info.encode())

        # server tells client to send the file if name is unique
        if self.sock.recv(1024).decode() == '1':
            # get contents of file
            file = open(fileName, "rb")

            # break file down into 1024 byte chunks
            chunk = file.read(1024)

            # send chunks of data until end
            while (chunk):
                self.sock.send(chunk)
                chunk = file.read(1024)
            time.sleep(1)
            self.sock.send('2'.encode())
            file.close()

        response = int(self.sock.recv(1024).decode())
        return response

    def delete(self, fileName):
        """
        Asks the data_retriever to delete a file

        :param fileName: name of the file you want deleted
        """

        info = json.dumps({'type':'delete',
                           'fileName': fileName})

        self.sock.send(info.encode())

        path = (str(os.path.abspath(fileName)))
        os.remove(path)


    def search(self, fileName):
        """
        Asks the data_retriever to search an existing file in the db

        :param fileName: name of file

        :return: contents of file, or an error msg if file doesn't exist
        """
        # initial msg
        info = json.dumps({'type': 'search',
                            'user': self.name,
                           'name': fileName,})

        self.sock.send(info.encode())

        # server tells client file 
        
        if self.sock.recv(1024).decode() == '1':

            file = open('files/' + fileName, 'w')
            #data = self.sock.recv(1024).decode()

            #keep recieving until EOF
            while(True):
                data = self.sock.recv(1024).decode()
                
                if data == '2':
                    file.close()
                    break
                else:
                    file.write(data)
            file.close()
            return 1
        else:
            return 0


    def edit(self, fileName, newFile):
        """
        Asks the data_retriever to replace content of a file

        :param fileName: name of existing file
        :param newFile: content that will replace fileName's content

        :return: relays the data_retriever's msg
        """
