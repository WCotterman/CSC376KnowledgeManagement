import sys, socket
class Upload:

    def upload(self,uF):
        #define connection
        HOST = 'localhost'
        PORT = 1120
        s = socket.socket()
        s.connect((HOST,PORT))

        #prepare file for transfer
        f=open (uF, "rb")
        #break file down into 1024 byte chunks
        chunk = f.read(1024)
        #send start of file flag
        s.send("SOF")
        #send file in 1024 byte chunks
        while (chunk):
            s.send(chunk)
            chunk = f.read(1024)
        #send End of File flag
        s.send("EOF")
        #close connection
        s.close()
