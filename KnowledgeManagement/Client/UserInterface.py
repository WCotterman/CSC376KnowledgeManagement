from Login import Login
from Upload import Upload
class UserInterface:
    def __init__(self, uin):
        self.self = self       

    def menuChoice():
        valid = ['U','S','E']
        while True:
            userChoice = str(input('What Would You Like To Do? ').upper())
            if userChoice in valid:
                UserInterface.inputCheck(userChoice)
                break
            else:
                print('Sorry But You Didnt Choose an available option... Try Again')

    def inputCheck(userChoice):
        if userChoice == str('U'):
            user  = Login().login()
            print('\n==========================================')
            print('               Welcome ' +str(user)+'!')
            print('     You Have Chosen to Upload a file.')
            print('==========================================')
            ui = str(input('Please enter a filename: '))
            Upload().upload(ui)
        
        if userChoice == str('S'):
            print('\n==========================================')
            print('You Have Chosen to Search the database!')
            print('==========================================')
            ui = str(input('Please enter a filename: '))
        
        if userChoice == str('E'):
            user  = Login().login()
            print('\n==========================================')
            print('               Welcome ' +str(user)+'!')
            print('You Have Chosen to Edit an existing file!')
            print('==========================================')
            ui = str(input('Please enter a filename: '))

    def main():
        print('==========================================')
        print('KNOWLEDGE MANAGEMENT SYSTEM')
        print('==========================================')
        print('Choose an option...')
        print('U. Upload  a file')
        print('S. Search for a file')
        print('E. Edit an existing file')
        UserInterface.menuChoice()        

UserInterface.main()
