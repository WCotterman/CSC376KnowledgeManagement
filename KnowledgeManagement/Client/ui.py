"""Handles the user inputs and calls each client function accordingly"""

from client import Client
import hashlib
import os

class UserInterface:

    def __init__(self, user):
        """
        Binds the UI object to a Client object so we can call
        client functions from within the UI class.

        :param user: an instantiated Client object
        """

        self.user = user

    def login(self):
        #MAIN login choice
        print("Choose an option...")
        print("L -> Login to existing account")
        print("C -> Create Account")
        print("E -> Exit")
        choice = str(input("What would you like to do? ")).lower()
        return choice

    def user_login(self):
        """
        Attempts to log self.user in OR calls register function for new user
        """
        choice=self.login()
        #choice=self.user_login_choice()
            # login
        if choice == 'l':
                username = str(input("Username: "))
                pword = str(input("Password: "))

                    # encrypt password before sending to server
                pword = hashlib.sha1(pword.encode()).hexdigest()
                    # call client login function
                response = self.user.login(username, pword)

                    # login didn't work, reloop
                if(response == 0):
                    #if username or pass wrong recalls user_login() function
                    print("Wrong username or password")
                    self.user_login()

                    # login worked, break out of loop
                else:
                    # store the user's info
                    self.user.name = username
                    print("Logged on!\n")

                        # break out of while loop after success
                        # ^^lies there is no while loop idk who wrote this but.....
            # new user
        elif choice == 'c':
            # call register function
            self.register()

            # improper input
        elif choice == 'e':
            # exit out of program
            os._exit(0)
        else:
            #if input is different
                print('Please enter a correct command')
                self.user_login()

    def register(self):
        '''
        Creates a new user
        '''

        while True:
            username = str(input("Create a username: "))
            pword = str(input("Create a password: "))
            # hash password
            pword = hashlib.sha1(pword.encode()).hexdigest()

            # inputs are both non-empty
            if (username and pword):
                # call client register function
                response = self.user.register(username, pword)

                # username already exists, reloop
                if(response == 0):
                    print('User name already exists, please enter a new one.')

                # creation worked
                else:
                    # store the user's info
                    self.user.name = username
                    print("Account created! \n")

                    # break out of while loop after success
                    break

            else:
                print("Please enter non-empty inputs")

    def menu_choice(self):
        """
        Verifies that the user enters in a correct command, then forwards
        the command to input_check
        """

        valid= ['U','R','S','D','Q']
        while True:
            choice = str(input('What would you like to do? ').upper())
            if choice in valid:
                self.input_check(choice)
                break
            else:
                print('Sorry that is not an available option... try again.')

    def input_check(self, choice):
        """
        Based on the user's command, the appropriate client function is called.

        :param choice: a string that is in ['U','S','D']

                       ^^^^ stop lying it should be ['U','S','D','Q'] < this Q
        """

        if choice == 'U':
            print('\n==========================================')
            print('You have chosen to upload a file!')
            print('==========================================')
            fileName = input('Please enter a filename: ')
            category = input('Please enter a category: ')
            keywords = input('Please enter keywords: ')

            response = self.user.upload(fileName, category, keywords)

            # results of upload
            if response == 1:
                print('Successful upload!\n')

            else: print('A file with that name already exists.\n')

        elif choice == 'R':
            print('\n==========================================')
            print('You have chosen to retrieve a file!')
            print('==========================================')
            file = str(input('Please enter a filename: '))

            response = self.user.download(file)
            if response == 1:
                print("Success!! file retrieved...\n")
            else:
                print ("Error!! cannot find file.. ")


        elif choice == 'S':
            print('\n==========================================')
            print('You have chosen to search for a file!')
            print('==========================================')
            file = str(input('Please enter a keyword to search for: '))
            if self.user.search(file):
                print("")


        elif choice == 'D':
            print('\n==========================================')
            print('You have chosen to delete an existing file!')
            print('==========================================')
            file = str(input('Please enter a filename: '))

            self.user.delete(file)
        else:
            os._exit(0)

if __name__ == "__main__":
    user = Client()
    UI = UserInterface(user)

    print('==========================================')
    print('KNOWLEDGE MANAGEMENT SYSTEM')
    print('==========================================')

    # login OR create account phase
    UI.user_login()

    # user logged in, now can do stuff
    while True:
        print('Choose an option...')
        print('U -> Upload  a file')
        print('R -> Retrieve  a file')
        print('S -> Search for a file')
        print('D -> Delete an existing file')
        print('Q -> Quit')
        UI.menu_choice()
