
DESC = """
\tMy dogshit script that use system32 app
"""

VERSION=    '0.0.2'
WLANSCMD=   "netsh wlan show profiles"
WLANKEYCMD= "netsh wlan show profile name=\"{}\" key=clear"

info=   """
> \tGETSH
> \tv0.0.1
> \tdesc:dumbish wrapper of netsh
> \tauthor:pipd0un
> \tcontact:pipdoun@gmail.com
"""

help=   """
-h\t\tshow list of valid arguments
-v\t\tshows short info of program
-list\t\tshows list of registered wlans
-get [arg]\tcalls get subprogram
\t\tthis arg can be an index number
\t\tif you passed this without arg this method will list all
\t\tof the wlan passwords you registered before
"""


SSIDLIST=   []
KEYLIST=    []
WLANDICT=   {}


def listwlan():
    i=1
    for wlan in SSIDLIST:
        print("["+str(i)+"] \t"+wlan)
        i+=1

def version():
    print(info)

def helpString():
    print(help)

def getall():
    print("********************************")
    for key in WLANDICT:
        print( "["+WLANDICT[key]+"]\t:\t["+key+"]")
    print("********************************")

def error(arg):
    print("********************************")
    print("[ ! ] "+arg)
    print("********************************")

argfun = {
    '-h': helpString,
    '-v': version,
    '-get': getall,
    '-list': listwlan,
}

if __name__ == "__main__":
    error("You are in library file.")