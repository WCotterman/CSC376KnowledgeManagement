"""the thread that handles the interaction b/w database and client"""

import threading
import json
from Server_Connections import connections

class DataRetriever( threading.Thread ):
    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connection = connection

    def run(self):
        # login
        while True:
            id = json.loads(self.connection.recv(1024).decode())
            if id['username'] == "Jack" and id['pword'] == "Klein":
                response = "OK"
            else:
                response = "NO"
            self.connection.send(response.encode())
            if response == "OK": break

