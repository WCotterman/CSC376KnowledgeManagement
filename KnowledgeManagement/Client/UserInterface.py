"""handles the user inputs and calls each Client function accordingly"""

from Client import Client

class UserInterface:

    def __init__(self, user):
        self.user = user

    # attempts to log user in
    def userLogin(self):
        while True:
            username = str(input("username: "))
            pword = str(input("password: "))
            response = self.user.login(username, pword)

            # login didn't work, retry
            if(response != "OK"):
                print("wrong username or password, please try again")

            # login worked, break out of function
            else:
                print("logged on!")
                break

    def menuChoice(self):
        valid = ['U','S','E']
        while True:
            userChoice = str(input('What Would You Like To Do? ').upper())
            if userChoice in valid:
                self.inputCheck(userChoice)
                break
            else:
                print('Sorry But You Didnt Choose an available option... Try Again')

    def inputCheck(self, userChoice):
        if userChoice == str('U'):
            print('\n==========================================')
            print('You Have Chosen to Upload a file!')
            print('==========================================')
            file = input('Please enter a filename: ')

            self.user.upload(file)

        if userChoice == str('S'):
            print('\n==========================================')
            print('You Have Chosen to Search the database!')
            print('==========================================')
            file = str(input('Please enter a filename: '))

            self.user.search(file)

        if userChoice == str('E'):
            print('\n==========================================')
            print('You Have Chosen to Edit an existing file!')
            print('==========================================')
            file = str(input('Please enter a filename: '))

            self.user.edit(file)

if __name__ == "__main__":
    user = Client() # init. the client
    UI = UserInterface(user) # init. the UI, passing the new user

    print('==========================================')
    print('KNOWLEDGE MANAGEMENT SYSTEM')
    print('==========================================')

    # login phase
    UI.userLogin()

    # user now logged in, can do stuff
    while True:
        print('Choose an option...')
        print('U. Upload  a file')
        print('S. Search for a file')
        print('E. Edit an existing file')
        UI.menuChoice()


