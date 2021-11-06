import sys
import numpy as np
import os
# import time
# from sknrf.device.instrument.shared.sg.ape.device import Device
# from sknrf.device.instrument.shared.sg.ape.gui import Control

np.set_printoptions(threshold=sys.maxsize)
n = 16384
dt = 1. / 1.28e9
t = np.arange(0, 16384 * dt, dt)
freq = 150e6
s = (1.1 * 8192 * np.sin(2 * np.pi * freq * t) + 32768 + 0.5)

yi = s.astype(int)
yi_lsb = yi & 255
yi_msb = (yi >> 8) & 255
f = np.stack((yi_lsb, yi_msb), axis=1)
yi_r = f.reshape(1, 32768)

yq = np.add(np.zeros((n,), dtype=int), 32768)
yq_lsb = yq & 255
yq_msb = (yq >> 8) & 255
f = np.stack((yq_lsb, yq_msb), axis=1)
yq_r = f.reshape(1, 32768)


# class RipTide(Device):
#     def __init__(self, host="172.16.0.160", port=9760):
#         super(self.__class__, self).__init__(host=host, port=port)
#         self.id = "{:s}:{:d}".format(host, port)
#         if not self.connected:
#             Control.instance().error("TCP/IP Server not started!")

def dec2hex(n):
    """return the hexadecimal string representation of integer n"""
    return "%X" % n

def hex2dec(s):
    """return the integer value of a hexadecimal string s"""
    return int(s, 16)

def crc(data):
    crc32 = np.array((hex2dec("FFFFFFFF")), dtype=np.uint32)
    poly = np.array((hex2dec("EDB88320")), dtype=np.uint32)
    data = np.array(data, dtype=np.uint8)
    data32 = np.array(data, dtype=np.uint32)
    datalength = data32.size

    rangelen = range(8)

    for i in range(datalength):
        crc32 = crc32 ^ data32[0, i]
        for j in rangelen:
            mask = ~(crc32 & np.array(1, dtype=np.uint32))
            if mask == 4294967295:
                mask = 0
            else:
                mask = mask + 1
            crc32 = np.array((crc32 >> 1) ^ (poly & mask), dtype=np.uint32)

    crc32 = ~(crc32)
    return crc32

crc1_q = crc(yq_r)
crc1_i = crc(yi_r)

wr_add = '08000000'
length = str(dec2hex(n - 1)).zfill(8)
# iqh = str(dec2hex((yi<<16)^(yq)).zfill(8))
h = (yi << 16) ^ yq
yt = np.array((h), dtype=np.uint32)
vhex = np.vectorize(hex)
iqh = vhex(yt)
crc_i = vhex(crc1_i)
crc_q = vhex(crc1_q)
iqh = np.array2string(yt, formatter={'int': lambda x: hex(x)})
crc_i = np.array2string(crc1_i, formatter={'int': lambda x: hex(x)})
crc_q = np.array2string(crc1_q, formatter={'int': lambda x: hex(x)})
removedBr = iqh[1:182954]
y1 = removedBr.strip()

def formatting(value):
    res = value
    li = [int(s, 16) for s in res.split()]
    ls = [f"{i:0>2x}" for i in li]
    result = "".join(ls)
    return result

y1 = (formatting(y1))
crc_i = (formatting(crc_i))
crc_q = (formatting(crc_q))
command_starter = "<<<<<<<<"
command_ender = ">>>>>>>>"
datatowrite = command_starter + wr_add + length + y1 + crc_i + crc_q + command_ender
datatowrite = datatowrite.upper()

fid = open('112.txt', 'w')
fid.write(datatowrite)
fid.close()

os.system("nc -q 0 172.16.0.160 9760 < /home/tilemasters/repos/sknrf-core/sknrf/device/instrument/lfsource/awg/112.txt")

