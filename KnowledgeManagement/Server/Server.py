import sys,socket,datetime,sqlite3,random
class Server:
    HOST = 'localhost'#define host
    PORT = 111#define port
    
    def createDatabase():
        #CREATE DATABASE IF IT DOESNT EXIST
        conn = sqlite3.connect('files.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS Files(ID TEXT, source TEXT, filename TEXT, category TEXT, keywords TEXT, timestamp TEXT)")

    def addToDatabase(uid,source,filename,category,keys):
        #ADD FILE ENTRY TO DATBASE
        timestamp = datetime.datetime.now()
        conn = sqlite3.connect('files.db')
        c = conn.cursor()
        c.execute("INSERT INTO Files VALUES (?, ?, ?, ?, ?, ?)", (int(uid),str(source),str(filename),str(category),str(keys),str(timestamp)))
        conn.commit()
        print("Item added to database")

    def get_posts():
        #PRINT DATABASE ENTRIES
        conn = sqlite3.connect('files.db')
        c = conn.cursor()
        c.execute("SELECT ID, source, filename, category, keywords, timestamp  from Files")
        conn.commit()
        for row in c:
            print(row)

            
    ##DEFINE SOCKET CONNECTION
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # define socket
    s.bind((HOST,PORT)) #bind host and port
    s.listen(10) # Accept 10 connections

    #HANDLE CONNECTION
    while True: # once connection is accepted:
        #display connected client
        sc, address = s.accept()
        print (address)
        ##ACCEPT PACKETS FROM CLIENT
        while (True):   
            #get filename (first 1024 bytes)
            fn = sc.recv(1024).decode()
            #create new empty file
            f = open(fn,'wb') #open and write to binary file

            ##PRINT DATABASE ENTRY INFO#####
            #get uid
            uid = random.random()*10
            print('filename received: '+ fn)
            #get Category(2nd 1024 bytes)
            cat = sc.recv(1024).decode()
            print('category received: '+ cat)
            #get keywords (3rd 1024 bytes)
            keys = sc.recv(1024).decode()
            print('keywords received: '+ keys)

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
            break

    s.close()
        
