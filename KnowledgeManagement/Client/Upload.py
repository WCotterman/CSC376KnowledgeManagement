import sys, socket

class Upload:
    
    def upload(self,uF):
        #define connection
        HOST = 'localhost'
        PORT = 114
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((HOST,PORT))
        #send filename
        s.send(uF.encode())
        #enter file category
        cat = str(input('Please enter a file category: '))
        s.send(cat.encode())
        #enter keywords
        keys = str(input('Please enter a list of keywords: '))
        s.send(keys.encode())
        
        #prepare file for transfer
        s.send("SOF".encode())
        f=open (uF, "rb")
        #break file down into 1024 byte chunks
        chunk = f.read(1024)
        #send file in 1024 byte chunks
        while (chunk):
            s.send(chunk)
            chunk = f.read(1024)
        print ("Done Sending")
        s.shutdown(socket.SHUT_WR)    
        ##s.send("EOF")
        #close connection
        d = s.recv(1024).decode()
        s.close()
        return d
