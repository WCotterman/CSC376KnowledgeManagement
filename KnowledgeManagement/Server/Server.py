import sys,socket
class Server:
    def openPacket(uin):
        print("doing stuff with the packet")
 
    
    HOST = 'localhost'#define host
    PORT = 8787#define port


    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM) # define socket
    s.bind((HOST,PORT)) #bind host and port
    s.listen(10) # Accept 10 connections
    while True: # once connection is accepted:
        #display connected client
        sc, address = s.accept()
        print (address)
        ext = '.'+'txt'
        #create new empty file
        f = open('received'+ext,'wb') #open and write to binary

        #load file with recieved data
        while (True):   
            #get filename
            fn = sc.recv(1024).decode()
            print('filename received: '+ fn)
            #get Category
            cat = sc.recv(1024).decode()
            print('category received: '+ cat)
            #get keywords
            keys = sc.recv(1024).decode()
            print('keywords received: '+ keys)
            #get start of file
            flag = sc.recv(3).decode()
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
                    #if packet is greater than 1 byte display received message
                    print("packet received")
            print("End of File Transfer..")
            f.close()
            break


                    #close file
            #f.close()
            #handle the packet
            #openPacket("test")
#close connection
    s.close()
        
