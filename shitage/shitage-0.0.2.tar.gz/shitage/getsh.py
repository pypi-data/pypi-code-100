from subprocess import Popen, PIPE
import consts as consts
import sys

def setWlanlist():
    with Popen( consts.WLANSCMD,
                universal_newlines=True,
                stdout=PIPE,
                shell=True) as ret:
        (out,err) = ret.communicate()
        if str(err) != "None":
            consts.error(err)
        lines = out.splitlines()
        for line in lines:
            if line.split(": ")[0].find("All User Profile") != -1:
                consts.SSIDLIST.append(line.split(": ")[1])

def setKeylist():
    found=0
    for ssid in consts.SSIDLIST:
        with Popen( consts.WLANKEYCMD.format(ssid),
                    universal_newlines=True,
                    stdout=PIPE,
                    shell=True) as ret:
            (out,err) = ret.communicate()
            if str(err) != "None":
                consts.error(err)
            lines = out.splitlines()
            for line in lines:
                if line.split(": ")[0] == "    Key Content            ":
                    consts.KEYLIST.append(line.split(": ")[1])
                    found=1
            if not found:
                consts.KEYLIST.append("[Empty]")
            if found:
                found=0
    pass

def setDict():
    i=0
    for addr in consts.SSIDLIST:
        consts.WLANDICT[addr] = consts.KEYLIST[i]
        i+=1

def keyOf(que):
    try:
        print("["+consts.WLANDICT[consts.SSIDLIST[que-1]]+"]")
    except:
        consts.error("INVALID INDEX")

def init():
    setWlanlist()
    setKeylist()
    setDict()

argc=   0

if __name__ == "__main__":
    init()
    
    argc=   len(sys.argv)

    if argc==   1:
        consts.error("getsh:\tNo Inputs.")
    elif argc== 2:
        found=  0
        for arg in consts.argfun:
            if sys.argv[1] == arg:
                consts.argfun[arg]()
                found=  1
        if not found:
            consts.error("INVALID ARGUMENT")
    elif argc==   3:
        if sys.argv[1] == '-get':
            if sys.argv[2].isdigit():
                keyOf(int(sys.argv[2]))
            else:
                consts.error("INVALID ARGUMENT")
        else:
            consts.error("INVALID ARGUMENT")
    else:
        consts.error("INVALID ARGUMENT")
    
    # python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*