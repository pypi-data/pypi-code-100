# This file is placed in the Public Domain.

import genocide.req as req
import genocide.slg as slg
import genocide.sui as sui
import genocide.trt as trt
import genocide.wsd as wsd

from gcd.tbl import Table


Table.addmod(req)
Table.addmod(slg)
Table.addmod(sui)
Table.addmod(trt)
Table.addmod(wsd)
