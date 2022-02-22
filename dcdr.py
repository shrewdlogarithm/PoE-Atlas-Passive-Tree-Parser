# GGG's ByteDecoder function translated into Python (only tested for v=6)
class dcdr:
    def __init__(self):
        self.dataString = ""
        self.position = 0

    def bytesToInt(self,t,e=4):
        i = 0
        for s in range (0,e):
            i += t[s]
            if s < e - 1:
                i = i << 8
        return i
    def bytesToInt16(self,t):
        return self.bytesToInt(t, 2)
    def hasData(self):
        return self.position < len(self.dataString)
    def getDataString(self):
        return self.dataString
    def setDataString(self,t):
        self.dataString = t
        self.position = 0
    def readInt8(self):
        return self.readInt(1)
    def readInt16(self):
        return self.readInt(2)
    def readInt(self,t=4):
        e = self.position + t
        if (e > len(self.dataString)):
            print("Integer read exceeds bounds")
        else:
            i = []
            for x in range (self.position,e):
                i.append(self.dataString[self.position])
                self.position = self.position + 1
            return self.bytesToInt(i, t)