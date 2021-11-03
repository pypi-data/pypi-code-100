import subprocess
import os

def HomeDirectory():
    return os.path.expanduser('~')

def command(args: list, quite=False, read=False):
    if quite:
        sub = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    elif read:
        sub = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                               stderr=subprocess.STDOUT)

        response = sub.communicate()[0].decode('utf8')
        sub.wait()
        sub.poll()
        returnCode = int(sub.returncode)

        return response, returnCode, sub
    else:
        sub = subprocess.Popen(args)

    sub.wait()
    sub.kill()
    sub.terminate()

def ip_address(interface='en0'):
    ip = command(['ipconfig', 'getifaddr', interface], read=True)
    ip = ip[0].removesuffix('\n')
    return ip

