import hashlib
class Login:
    #load dictionary from SQLITE .db file instead of hardcoded
    validUsers = {"user1":"password1", "user2":"password2", "user3":"password3", "user4":"password4","user5":"password5"}
    
    def login (self):
        while True:
            user = str(input("\nEnter login name: "))
            passw = str(input("Enter password: "))

            #hash user input password to compare against hashed database passwords
            mdpass = hashlib.md5(passw.encode()).hexdigest()
    
            # check if user exists and login matches password
            if user in Login.validUsers and passw == Login.validUsers[user]:
                return user
            else:
                print ("\nUser doesn't exist or wrong password!\n")

    
