#! /usr/bin/env python

from socketMaster import dataServer

sn_ip = '192.168.217.203'      # SHARKNINJA
hm_ip = '192.168.109.128'      # HOME VM

ser = dataServer(sn_ip, 5050)
ser.start()
