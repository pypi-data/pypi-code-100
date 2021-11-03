#! /usr/bin/python

from socketMaster import client
from dataSupervisor import dataSupervisor
from SKU import CFP
from sample_data.sample_data import data

sn_ip = '192.168.217.203'      # SHARKNINJA
hm_ip = '192.168.109.128'      # HOME VM

cfp = CFP()

super = dataSupervisor(headers=False, s3_enable=False)
super.set_product_map(cfp.queries)
super.lst = data

super.interpreted_parse()

cli = client(sn_ip, 5050)
cli.send_msg(cli.node, super.df)
cli.send_msg(cli.node, '!DC')
