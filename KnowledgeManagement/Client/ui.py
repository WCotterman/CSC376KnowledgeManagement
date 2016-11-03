"""Handles the user inputs and calls each client function accordingly"""

from client import Client

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
        Attempts to log self.user in
        """

        while True:
            username = str(input("username: "))
            pword = str(input("password: "))
            response = self.user.login(username, pword)

            # login didn't work, reloop
            if(response != "OK"):
                print("Wrong username or password, please try again.")

            # login worked, break out of loop
            else:
                self.user.name = username # store the user's name in a property
                print("Logged on!")
                break

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

    # login phase
    UI.user_login()

    # user logged in, now can do stuff
    while True:
        print('Choose an option...')
        print('U -> Upload  a file')
        print('S -> Search for a file')
        print('E -> Edit an existing file')
        UI.menu_choice()


