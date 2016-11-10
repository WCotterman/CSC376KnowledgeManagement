"""All the functions that a user can perform.
   The client object gets instantiated and used in ui.py"""

import socket
import json

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
        info = json.dumps({'type': 'login', 'username': username, 'pword': pword})
        self.sock.send(info.encode())

        # wait for response
        response = int(self.sock.recv(1024).decode())
        return response

    def register(self, username, pword):
        '''
        Registers a new user

        :param username: new user name
        :param pword: new user password

        :return: 0 if username is not unique (can't have duplicate usernames)
                 1 if username is unique and user is put in db
        '''

        # serialize the username and pword into json
        info = json.dumps({'type': 'register', 'username': username, 'pword': pword})
        self.sock.send(info.encode())

        # wait for response
        response = int(self.sock.recv(1024).decode())
        return response

    def upload(self, fileName, file):
        """
        Asks the data_retriever to upload a file to the db

        :param fileName: name of new file
        :param file: contents of new file

        :return: relays the data_retriever's msg
        """

    def search(self, fileName):
        """
        Asks the data_retriever to search an existing file in the db

        :param fileName: name of file

        :return: contents of file, or an error msg if file doesn't exist
        """

    def edit(self, fileName, newFile):
        """
        Asks the data_retriever to replace content of a file

        :param fileName: name of existing file
        :param newFile: content that will replace fileName's content

        :return: relays the data_retriever's msg
        """
