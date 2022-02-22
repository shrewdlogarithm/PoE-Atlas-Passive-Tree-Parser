import base64,re,json,os
from urllib.parse import unquote
from dcdr import dcdr
import requests

vers = "3_17"
currentversion = 6 # not enirely sure how/where this was set in the original code but '6' seems to be the value we need!!

incleagues = ["Archnemesis","SSF Archnemesis","Hardcore Archnemesis","SSF Archnemesis HC"]

adbname = "atlas-skill-tree" + vers + ".json"
adb = {}
if os.path.exists(adbname):
    with open(adbname) as json_file:
        adb = json.load(json_file)
adbn = adb["nodes"]

ndbname = "acctdb.json"
ndb = {}

poesite = 'https://www.pathofexile.com'
session = requests.Session()
session.headers.update({'User-Agent': 'PoEApt'})

if os.path.exists(ndbname):
    with open(ndbname) as json_file:
        ndb = json.load(json_file)
else:
    accounts = [
        "mathil",
        "zizaran",
        "bigducks",
        "yojimoji",
        "steelmage",
        "raizqt",
        "ghazzy",
        "thisisbadger",
        "notscarytime",
        "donthecrown",
        "pohx",
        "nugiyen",
        "octavian0",
        "thi3n",
        "baker",
        "catmaster",
        "balormage",
        "AsmodeusPOE",
        "ventrua",
        "Karvarousku",
        "navandis",
        "TheVictor003",
        "dslily",
        "alkaizerx",
        "darkee",
        "goratha",
        "jorgo44"
    ]


    for account in accounts:
        apichars = session.get(f"{poesite}/character-window/get-characters?accountName={account}&realm=pc")
        if apichars.status_code != 200:
            print(f'Error: failed to read characters for account {account}')
        else:
            leagues = []
            apichardb = apichars.json()
            for apichar in apichardb:
                if "league" in apichar and apichar["league"] in incleagues and apichar["league"] not in leagues:
                    leagues.append(apichar["league"])            
            for league in leagues:

                response = session.get(f"{poesite}/character-window/view-atlas-skill-tree?accountName={account}&realm=pc&league={league}")

                if response.status_code == 200:
                    # this is redirected to a URL which contains the string which we extract below
                    e = re.sub(r'.*\/', '', response.url)    

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
                            l.append(str(n.readInt16()))
                        u = n.readInt8()
                        for d in range(0,u):
                            o.append(n.readInt16())
                        v = n.readInt8()
                        for d in range(0,v):
                            f = n.readInt()
                            h[65535 & f] = f >> 16
                    else:
                        print("The build you are trying to load is using an old version of the passive tree and will not work.")

                    print("Scanning ", account,league)
                    for an in l:
                        if an in adbn:
                            if "isNotable" in adbn[an]:
                                if an in ndb:
                                    ndb[an]["count"] += 1
                                    ndb[an]["acts"].append(account + "-" + league)
                                else:
                                    ndb[an] = {
                                        "count": 1,
                                        "acts": [account + "-" + league]
                                    }
                with open(ndbname, 'w') as json_file:
                    json.dump(ndb, json_file, indent=4) 

for n in sorted(ndb.items(),key=lambda x:x[1]["count"],reverse=True):
    groupname = ""
    if "group" in adbn[n[0]] and str(adbn[n[0]]["group"]) in adb["groups"]:
        group = adb["groups"][str(adbn[n[0]]["group"])]
        for node in group["nodes"]:
            if "isMastery" in adbn[node]:
                groupname = adbn[node]["name"]
                break
    print(ndb[n[0]]["count"],adbn[n[0]]["name"],"-",groupname)
