""" All the sqlite3 functions needed for querying the db (encapsulates the sql code)
    DB object used by the data_retriever"""

import sqlite3
import datetime

class DB:

        def __init__(self):
                # establish a connection w/ the database (check_same_thread=False is possibly sketchy, needs more research)
                self.conn = sqlite3.connect('database.db', check_same_thread=False)

                # create the tables if not already in DB
                self.conn.execute('''CREATE TABLE IF NOT EXISTS USERS
                    (username   TEXT PRIMARY KEY  NOT NULL,
                    pword       TEXT              NOT NULL);''')

                self.conn.execute('''CREATE TABLE IF NOT EXISTS FILES
                    (ID         TEXT,
                     filename   TEXT PRIMARY KEY  NOT NULL,
                     category   TEXT,
                     keywords   TEXT,
                     timestamp  TEXT);''')

                self.conn.commit()

        def login(self, username, pword):
                '''
        Attempts to find an entry in the USERS table with the given parameters

        :param username: username entered by user
        :param pword: password entered by user

        :return: 0 if username doesn't exist or incorrect password OR
                 1 if username exists and enters correct password
		'''

                cursor = self.conn.execute("SELECT * FROM USERS WHERE username == ? AND pword == ?", (username, pword))

# user will either be the one result, or 'None'
                user = cursor.fetchone()
                if user == None:
                        return 0
                elif user[0] == username:
                        return 1

                # backup catchall if for some reason the returned username != input username
                else:
                        return 0

        def register(self, username, pword):
                '''
        Attempts to enter a new username and pword into the USERS table

        :param username: new username, MUST BE UNIQUE
        :param pword: new password

        :return: 0 if username is not unique (can't have duplicate usernames)
                 1 if username is unique and user is put in db
		'''

                try:
                        self.conn.execute("INSERT INTO USERS(username, pword) VALUES(?,?)", (username, pword))
                        self.conn.commit()
                        return 1
                # username is not unique
                except sqlite3.IntegrityError:
                        return 0

        def upload(self, id, fileName, category, keywords):
                '''
        Inserts new file into the FILES table

        :param id: username of user who's uploading file
        :param fileName: name of file
        :param category: category of file
        :param keywords: keywords

        :return: 0 if upload is not successful (can't have duplicate fileNames)
                 1 if upload is successful
		'''

                timestamp = datetime.datetime.now()

                try:
                        self.conn.execute("INSERT INTO FILES VALUES(?,?,?,?,?)", (id, fileName, category, keywords, timestamp))
                        self.conn.commit()
                        return 1

	# fileName not unique
                except sqlite3.IntegrityError:
                        return 0

        def delete(self,fileName):
                '''
        Attempts to delete fileName from the FILES table

        :param fileName: name of file

		:return: 0 if file is not found
                 1 if the file is found in the FILES table and is deleted
		'''
                try:
                        cursor = self.conn.execute("DELETE FROM FILES WHERE filename=?",(fileName,))
                        self.conn.commit()

                # fileName not found
                except sqlite3.Error:
                        return 0

				
        def search (self, query):
                '''
        Attempts to query for file existence.

        :param fileName: name of file

        :return: 0 if file is not found
                 1 if the file is found in the FILES table and is deleted
		'''
                try:
                        print("searching database")
                        cursor = self.conn.execute("SELECT id,filename,timestamp FROM FILES WHERE keywords like '%"+query+"%'")
                        self.conn.commit()
                        result = cursor.fetchall()
                        return result

        # fileName not found
                except sqlite3.Error:
                        return 0
        
