import datetime
class Packet:
    def __init__(length,source,time,uniqueID,category,file64):
        self.length = length
        self.source = source
        self.time = datetime.datetime.now()
        self.uniqueID = uniqueID
        self.category = category
        self.file64 = file64

    
