# PoE Atlas Passive Tree Parser

This is just an example to show how to parse the 'string' GGG use for the Atlas Passive Tree into the actual Node numbers 

atlas-skill-tree3_17.json is the GGG Atlas Passive database keyed by Node number with information on name/what it does/what it links-to etc.
 
aptest.js shows how to parse the Atlas Passive Tree 'string' for a given account/league in the browser (has CORS issues as we're not GGG!)

aptest.node.js is the same as aptest.js other than being converted to work from Node.JS (no CORS issues)



Python Conversions...

aptest.py - aptest.js converted into Python
dcdr.py - Python version of the ByteDecoder

sumnotables.py - loads Atlas Passive Trees for a selection of streamers and shows the most popular nodes chosen (and stores the results for later reuse)
Note: there's no rate-limiting done here so you could easily get blocked if you run this too-often/on too many accounts...


