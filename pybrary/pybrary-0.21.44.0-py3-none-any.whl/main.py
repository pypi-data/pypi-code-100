from sys import argv

import pybrary


def parse_argv():
    cmd, fct, *opt = argv
    args, kw = [], {}
    for o in opt:
        if '=' in p:
            k, v = o.split('=')
            kw[k] = v
        else:
            args.append(o)
    return cmd, fct, args, kw


def get_ip_adr():
    try:
        ok, adr = pybrary.get_ip_adr()
        if ok:
            print(adr)
        else:
            print('ERROR : %s' % adr)
    except Exception as x:
        print('Exception ! %s' % x)
