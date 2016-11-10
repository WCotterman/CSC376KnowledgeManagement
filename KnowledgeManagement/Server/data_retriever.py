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
        Handles the interaction with the client. First it verifies the login,
        then it starts receiving requests for files

        info is a python dictionary used for logging user in:
            KEYS
            'type' : either 'login' or 'register'
            'username'
            'pword'
        """

        # login loop
        while True:
            info = self.connection.recv(1024).decode()
            # turns info (a json string) into a python dictionary
            info = json.loads(info)

            username = info['username']
            pword = info['pword']

            # determine if user is logging in or creating new user
            if(info['type'] == 'login'):
                response = self.db.login(username, pword)
            else:
                response = self.db.register(username, pword)

            # must turn int into str to send over the socket
            self.connection.send(str(response).encode())

            # only break login loop when login/register is successful
            if response == 1:
                break

        # next loop will handle client requests


    def upload(self, fileName, source, file, category=None, keys=None):
        """
        Inserts the new file into the db

        :param fileName: name of new file
        :param source: filepath of the new file
        :param file: contents of new file
        :param category(optional): file category, for top level organization
        :param keys(optional): keywords for search functions

        :return: a msg indicating success or not
        """

        #create new empty file
        f = open(fileName,'wb') #open and write to binary file

        ##PRINT DATABASE ENTRY INFO#####
        #get uid
        uid = random.random()*10

        ####GET FILE FROM TRANSFER ######
        #get start of file
        flag = sc.recv(3).decode() #start of file 3 byte flag
        if(flag  == "SOF"):
            print("Start of file transfer")
            #get file data
            data = sc.recv(1024)
            while (data):
                #print (data)
                #write recieved data to file
                f.write(data)
                #receive next 1024 bytes
                data = sc.recv(1024)
                print("packet received")
        print("End of File Transfer..")
        #close file
        f.close()

        #CREATE DATABASE IF NON EXISTANT
        createDatabase()
        #ADD FILE TO DATABASE
        addToDatabase(int(uid),address,fn,cat,keys)
        #PRINT DATABASE ENTRIES
        get_posts()

    #todo: return success token

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

    def createDatabase(self):
        """Create the database if it doesn't already exist"""
        conn = sqlite3.connect('files.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS Files(ID TEXT, source TEXT, filename TEXT, category TEXT, keywords TEXT, timestamp TEXT)")

    def addToDatabase(self, uid, source, filename, category=None, keys=None):
        """
        Add file entry to database

        :param uid: unique identifier for file
        :param source: filepath of the new file
        :param filename: name of new file
        :param category(optional): file category, for top level organization
        :param keys(optional): keywords for search functions
        """
        timestamp = datetime.datetime.now()
        conn = sqlite3.connect('files.db')
        c = conn.cursor()
        c.execute("INSERT INTO Files VALUES (?, ?, ?, ?, ?, ?)", (int(uid),str(source),str(filename),str(category),str(keys),str(timestamp)))
        conn.commit()
        print("Item added to database")

    #todo: return success token

    def get_posts(self):
        """Print all database entries"""
        conn = sqlite3.connect('files.db')
        c = conn.cursor()
        c.execute("SELECT ID, source, filename, category, keywords, timestamp  from Files")
        conn.commit()
        for row in c:
            print(row)
