"""A thread that handles the interaction b/w the database and one client"""
import os
import time
import threading
import json
import datetime
import sqlite3
import random
import hashlib
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

                    # keep recieving until EOF
                    while(True):
                        data = self.connection.recv(1024).decode()

                        # 2 = EOF
                        if data == '2':
                            break

                        else: file.write(data)

                    file.close()
                    print ("upload retrieved..")

                # else tell the client not to send over the file (duplicate)
                else:
                    self.connection.send('0'.encode())

            elif type == 'download':
                fileName = info['fileName']
                path = "files/"+fileName

                if os.access(path, os.R_OK):
		#send back file to client
                    print("Success! Starting File Transfer..")
                    self.connection.send('SOF'.encode())
                    self.sendFile(info['fileName'])


                else:
                    print("Error! The file was not found.. please verify the file exists")
                    self.connection.send('FNF'.encode())



            elif type == 'search':
                query = info['query']

                if self.db.search(query):
		#send back file to client
                    print("Success! The file was found")
                    self.connection.send('SOQ'.encode())
                    self.sendQuery(query)
                else:
                    print("Error! The file was not found.. please verify the file exists")
                    self.connection.send('FNF'.encode())



            elif type == 'delete':
                fileName = info['fileName']

                response = self.db.delete(fileName)

                if response == 0:
                    print("The file was not deleted. Verify that the file exists.")
                else:
                    print("The file was deleted")
            self.connection.send(str(response).encode())



    def sendFile(self, fileName):
        print("sending file to client..")
        self.connection.send('SOF'.encode())

        file = open('files/'+fileName, "rb")

        # break file down into 1024 byte chunks
        chunk = file.read(1024)
        # send chunks of data until end
        while (chunk):
            self.connection.send(chunk)
            chunk = file.read(1024)
        time.sleep(1)
        self.connection.send('EOF'.encode())
        file.close()

    def sendQuery(self,query):
        print("sending search results to client..")
        self.connection.send('SOQ'.encode())

        result = self.db.search(query)
        result = json.dumps(result)

        self.connection.send(result.encode())
        self.connection.send('SOQ'.encode())


    def edit(self, fileName, newFile):
        """
        Replaces the content of a file in the db

        :param fileName: name of existing file
        :param newFile: content that will replace fileName's content

        :return: a msg indicating success or not
        """
