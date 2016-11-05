"""A thread that handles the interaction b/w the database and one client"""

import threading
import json
import sys,socket,datetime,sqlite3,random
from connections import connections

class DataRetriever( threading.Thread ):
    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connection = connection

    def run(self):
        """
        Handles the interaction with the client. First it verifies the login,
        then it starts receiving requests for files
        """

        # login loop
        while True:
            info = self.connection.recv(1024).decode()
            response = self.login(info)
            self.connection.send(response.encode())

            # only break loop when login is verified
            if response == "OK":
                break

        # next loop will handle client requests

    def login(self, info):
        """
        Queries db to verify user login info

        :param info: a json object consisting of a username and pword

        :return: "OK" if username exists and enters correct password OR
                 "NO" if username doesn't exist or password incorrect
        """

        # turns info into a python dictionary
        info = json.loads(info)

        # this is just a test, haven't connected to DB yet
        if info['username'] == "Jack" and info['pword'] == "Klein":
            return "OK"
        else:
            return "NO"

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
