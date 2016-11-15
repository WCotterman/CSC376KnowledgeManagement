"""A thread that handles the interaction b/w the database and one client"""

import threading
import json
import datetime
import sqlite3
import random
from connections import connections
from db import DB

class DataRetriever( threading.Thread ):

    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connection = connection

        # establish a database connection
        self.db = DB()

    def run(self):
        """
        Handles the interaction with the client.
            - login
            - register new user
            - upload file
            - edit file
            - search file

        * self.connection first receives a dictionary named 'info' *
            - info dict always has key 'type'
        """

        while True:
            info = self.connection.recv(1024).decode()
            info = json.loads(info)
            # type is VERY important
            type = info['type']

            response = ""
            if type == 'login':
                username = info['username']
                pword = info['pword']
                response = self.db.login(username, pword)

            elif type == 'register':
                username = info['username']
                pword = info['pword']
                response = self.db.register(username, pword)

            elif type == 'upload':
                # file upload parameters for fb
                id = info['user']
                fileName = info['name']
                category = info['category']
                keywords = info['keywords']

                response = self.db.upload(id, fileName, category, keywords)

                # file name is unique, accept file
                if response == 1:
                    # tell client to send the file
                    self.connection.send('1'.encode())

                    # create the file on server side
                    file = open('files/' + info['name'], 'w')

                    # receive contents of the file
                    data = self.connection.recv(1024).decode()
                    file.write(data)

                    # TODO PROTOCOL FOR END OF FILE
                    # while(data):
                    #     # 1 = end of file (IMPORTANT)
                    #     if data == 1:
                    #         break
                    #     else:
                    #         file.write(data)
                    #         # receive next chunk of file (or EOF flag)
                    #         data = self.connection.recv(1024).decode()

                    file.close()

                # else tell the client not to send over the file
                else:
                    self.connection.send('0'.encode())

            self.connection.send(str(response).encode())



    def search(self, fileName):
        """
        Queries the db for a file

        :param fileName: name of the file

        :return: contents of the file, or an error msg
        """

    def edit(self, fileName, newFile):
        """
        Replaces the content of a file in the db

        :param fileName: name of existing file
        :param newFile: content that will replace fileName's content

        :return: a msg indicating success or not
        """
