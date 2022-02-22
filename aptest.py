import base64,re
from urllib.parse import unquote
import requests

# First we get the 'Atlas Passive String' from the POE website

act = "zizaran"
league = "SSF Archnemesis HC"
currentversion = 6 # not enirely sure how/where this was set in the original code but '6' seems to be the value we need!!

url = "https://www.pathofexile.com/character-window/view-atlas-skill-tree?accountName=" + act + "&realm=pc&league=" + league


session = requests.Session()
session.headers.update({'User-Agent': 'PoEApt'})
response = session.get(url)

if response.status_code == 200:
    # this is redirected to a URL which contains the string which we extract below
    e = re.sub(r'.*\/', '', response.url)

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

    # translated from GGG's code to decode the string
    e = base64.b64decode(e.replace("-","+").replace("_","/"))

    n = dcdr()
    n.setDataString(e)
    s = 0
    a = 0
    r = 0
    l = []
    o = []
    h = []

    v = n.readInt()
    if v == 4:
        s = n.readInt8()
        a = n.readInt8()
        r = n.readInt8()
        while n.hasData():
            l.append(n.readInt16())
    elif v == 5:
        s = n.readInt8()
        a = n.readInt8()
        c = n.readInt8()
        for d in range(0,c):
            l.append(n.readInt16())
        u = n.readInt8()
        for d in range(0,u):
            o.append(n.readInt16())
    elif v == currentversion:
        s = n.readInt8()
        a = n.readInt8()
        c = n.readInt8()
        for d in range(0,c):
            l.append(n.readInt16())
        u = n.readInt8()
        for d in range(0,u):
            o.append(n.readInt16())
        v = n.readInt8()
        for d in range(0,v):
            f = n.readInt()
            h[65535 & f] = f >> 16
    else:
        print("The build you are trying to load is using an old version of the passive tree and will not work.")

    print(l)