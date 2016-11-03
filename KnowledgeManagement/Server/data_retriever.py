"""A thread that handles the interaction b/w the database and one client"""

import threading
import json
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

    def upload(self, fileName, file):
        """
        Inserts the new file into the db

        :param fileName: name of new file
        :param file: contents of new file

        :return: a msg indicating success or not
        """

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
