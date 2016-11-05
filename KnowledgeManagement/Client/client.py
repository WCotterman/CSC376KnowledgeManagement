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

        :return: "OK" or "NO" depending on what the data_retriever returns
        """

        # serialize the username and pword into json
        info = json.dumps({'username': username, 'pword': pword})
        self.sock.send(info.encode())

        # wait for response
        response = self.sock.recv(1024).decode()
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
