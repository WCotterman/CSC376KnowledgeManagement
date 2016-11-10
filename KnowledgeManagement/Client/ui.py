"""Handles the user inputs and calls each client function accordingly"""

from client import Client
import hashlib

class UserInterface:

    def __init__(self, user):
        """
        Binds the UI object to a Client object so we can call
        client functions from within the UI class.

        :param user: an instantiated Client object
        """

        self.user = user

    def user_login(self):
        """
        Attempts to log self.user in OR calls register function for new user
        """

        choice = str(input("Do you already have an account? (y/n) ")).lower()

        while True:

            # login
            if choice == 'y':
                while True:
                    username = str(input("Username: "))
                    # encrypt the password
                    pword = hashlib.sha224(str(input("Password: "))).hexdigest()

                    # encrypt password before sending to server

                    # call client login function
                    response = self.user.login(username, pword)

                    # login didn't work, reloop
                    if(response == 0):
                        print("Wrong username or password, please try again.")

                    # login worked, break out of loop
                    else:
                        # store the user's info
                        self.user.name = username
                        self.user.pword = pword
                        print("Logged on!\n")

                        # break out of while loop after success
                        break
                break

            # new user
            elif choice == 'n':
                # call register function
                self.register()
                break

            # improper input
            else:
                print('Please enter a correct command (y/n)')
                choice = str(input('Do you already have an account? ')).lower()

    def register(self):
        '''
        Creates a new user
        '''

        while True:
            username = str(input("Create a username: "))
            pword = str(input("Create a password: "))

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
                    self.user.pword = pword
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

        valid = ['U','S','E']
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

        :param choice: a string that is in ['U','S','E']
        """

        if choice == 'U':
            print('\n==========================================')
            print('You have chosen to upload a file!')
            print('==========================================')
            file = input('Please enter a filename: ')

            #self.user.upload(file)

        elif choice == 'S':
            print('\n==========================================')
            print('You have chosen to search the database!')
            print('==========================================')
            file = str(input('Please enter a filename: '))

            #self.user.search(file)

        else: # choice == 'E'
            print('\n==========================================')
            print('You have chosen to edit an existing file!')
            print('==========================================')
            file = str(input('Please enter a filename: '))

            #self.user.edit(file)

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
        print('S -> Search for a file')
        print('E -> Edit an existing file')
        UI.menu_choice()


