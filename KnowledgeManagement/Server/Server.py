import sys,socket
class Server:
    def openPacket(uin):
        print("doing stuff with the packet")

    
    HOST = 'localhost'#define host
    PORT = 1120 #define port


    s = socket.socket() # define socket
    s.bind((HOST,PORT)) #bind host and port
    s.listen(10) # Accept 10 connections
    a=0
    while True: # once connection is accepted:
        #display connected client
        sc, address = s.accept()
        print address

        #create new empty file
        f = open('received.txt','wb') #open in binary

        #load file with recieved data
        while (True):   
            #get first 3 bytes for size
            flag = sc.recv(3)
            #load 1024 bytes
            l = sc.recv(1024)
            if flag  == "SOF":
                print("Start of file transfer")
                while (l):
                    #write recieved data to file
                    f.write(l)
                    #receive next 1024 bytes
                    l = sc.recv(1024)
                    #if packet is greater than 1 byte display recieved message
                    if sys.getsizeof(l) > 1:
                        print("packet received")
            #close file
            f.close()
            #handle the packet
            #openPacket("test")
#close connection
    s.close()
        
