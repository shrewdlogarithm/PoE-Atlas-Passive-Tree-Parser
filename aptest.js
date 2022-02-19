// First we get the 'Atlas Passive String' from the POE website

var act = "YOURACCOUNTNAMEOFCHOICE"
var league = "THECURRENTLEAGUENAME"
var currentversion = 6 // not enirely sure how/where this was set in the original code but '6' seems to be the value we need!!


var url = "https://www.pathofexile.com/character-window/view-atlas-skill-tree?accountName=" + act + "&realm=pc&league=" + league

fetch(url, { method: 'GET' })
    .then(response => {
        // this is redirected to a URL which contains the string which we extract below
        var e = response.url.replace(/.*\//,"")            

        // GGG's ByteDecoder function converted from RequireJS
        var dcdr = function() {
            this.init = function() {
                this.dataString = "",
                this.position = 0
            };
            this.bytesToInt16 = function(t) {
                return this.bytesToInt(t, 2)
            };
            this.bytesToInt = function(t, e) {
                e = e || 4;
                for (var i = 0, s = 0; s < e; ++s)
                    i += t[s],
                    s < e - 1 && (i <<= 8);
                return i
        };
            this.hasData = function() {
                return this.position < this.dataString.length
            };
            this.getDataString = function() {
                return this.dataString
            };
            this.setDataString = function(t) {
                this.dataString = t,
                this.position = 0
            };
            this.readInt8 = function() {
                return this.readInt(1)
            };
            this.readInt16 = function() {
                return this.readInt(2)
            };
            this.readInt = function(t) {
                t = t || 4;
                var e = this.position + t;
                if (e > this.dataString.length)
                    throw "Integer read exceeds bounds";
                for (var i = []; this.position < e; ++this.position)
                    i.push(this.dataString.charAt(this.position).charCodeAt(0));
                return this.bytesToInt(i, t)
            };
            this.init()
        }

        // GGG's code to decode the string
        e = decodeURIComponent(e.replace(/-/g, "+").replace(/_/g, "/"));
        try {
            e = atob(e) // simplified from GGGs slightly odd implementation
        } catch (t) {
            this.errorMessage = "Failed to load build from URL. Please make sure it was copied correctly.";
        }

        var s, a, n = new dcdr;
        n.setDataString(e);
        var r = 0
        , l = []
        , o = []
        , h = {};

        switch (n.readInt()) {
            case 4:
                for (s = n.readInt8(),
                    a = n.readInt8(),
                    r = n.readInt8(); n.hasData(); )
                    l.push(n.readInt16());
                break;
            case 5:
                s = n.readInt8(),
                    a = n.readInt8();
                for (var c = n.readInt8(), d = 0; d < c; ++d)
                    l.push(n.readInt16());
                var u = n.readInt8();
                for (d = 0; d < u; ++d)
                    o.push(n.readInt16());
                break;
            case currentversion:
                s = n.readInt8(),
                    a = n.readInt8();
                for (c = n.readInt8(),
                    d = 0; d < c; ++d)
                    l.push(n.readInt16());
                for (u = n.readInt8(),
                    d = 0; d < u; ++d)
                    o.push(n.readInt16());
                var v = n.readInt8();
                for (d = 0; d < v; ++d) {
                    var f = n.readInt();
                    h[65535 & f] = f >>> 16
                }
                break;
            default:
                alert("The build you are trying to load is using an old version of the passive tree and will not work.")
        }

        console.log(l); // variable 'l' contains the list of nodes we need
    })
    .catch(function(err) {
        console.info(err + " url: " + url);
    });
