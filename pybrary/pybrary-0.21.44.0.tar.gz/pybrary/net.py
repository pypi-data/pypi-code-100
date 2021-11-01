from urllib.request import urlopen

from . import logger, debug, error

def get_ip_adr():
    url = 'http://api.ipify.org'
    with urlopen(url, timeout=1) as resp:
        if resp.status==200:
            adr = resp.read().decode().strip()
            debug('ip adr : %s', adr)
            return True, adr
        else:
            error('%s %s', resp.status, resp.reason)
            return False, resp.reason
