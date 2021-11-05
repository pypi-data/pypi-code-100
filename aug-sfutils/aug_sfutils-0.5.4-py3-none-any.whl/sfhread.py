import os, logging
from struct import unpack
import numpy as np
from aug_sfutils import sfdics, str_byt

n_rel = 8

logger = logging.getLogger('aug_sfutils.sfhread')


def read_sfh(byt_str):
    """
    Reads a full shotfile header
    """

    sfhead = {}
    obj_names = []
    n_max = 1000
    n_obj = n_max
    for j in range(n_max):
        sfo = SFH_READ(byt_str[j*128: (j+1)*128])
        sfo.objid = j
        typ =  sfo.obj_type
        onam = str_byt.to_str(sfo.objnam.strip())
        if typ == 1:
            sfo.diag()
            if n_obj == n_max:
                n_obj = sfo.num_objs
        elif typ == 2:
            sfo.list()
        elif typ == 3:
            sfo.device()
        elif typ == 4:
            sfo.parmset()
        elif typ == 5:
            sfo.mapping()
        elif typ in (6, 7):
            sfo.sig()
        elif typ == 8:
            sfo.tbase()
        elif typ == 9:
            sfo.sf_list()
        elif typ == 10:
            sfo.algorithm()
        elif typ == 11:
            sfo.update_set()
        elif typ == 12:
            sfo.loctimer()
        elif typ == 13:
            sfo.abase()
        elif typ == 14:
            sfo.qualifier()
        elif typ == 18:
            sfo.addrlen()
        sfhead[onam] = sfo
        obj_names.append(onam)
        if j == n_obj - 1:
            break

    for onam, sfo in sfhead.items():
        sfo.relations = [obj_names[jid] for jid in sfo.rel if jid != 65535]

    return sfhead


class SFH_READ:
    """
    Reads a generic object's metadata from the SFH's byte string
    """

    def __init__(self, byte_str):
        """
        Reads the SFH part of an object, common to all objects
        """
        self.objnam   = str_byt.to_str(byte_str[0:8].strip())
        self.obj_type, self.level, self.status = unpack('>3H', byte_str[ 8: 14])
        if self.obj_type in sfdics.obj_name.keys():
            self.object_type = sfdics.obj_name[self.obj_type]
        else:
            self.object_type = 'Unknown'
        self.errcode  = unpack('>h', byte_str[14: 16])[0]
        fmt = '>%dH' %n_rel
        self.rel      = unpack(fmt,  byte_str[16        : 16+2*n_rel])
        self.address, self.length = unpack('>2I', byte_str[16+2*n_rel: 24+2*n_rel])
        self.val      = byte_str[40:  64]
        self.descr    = str_byt.to_str(byte_str[64: 128].strip())


    def diag(self):
        """
        Metadata of a DIAG object
        """
        self.diag_code = self.val[: 4]
        self.num_objs, self.diag_type  = unpack('>2H', self.val[4: 8])
        self.shot_nr , self.c_time     = unpack('>2I', self.val[8: 16])
        self.up_limit, self.exp, self.version, self.s_type = unpack('>4H', self.val[16: 24])


    def list(self):
        """
        Metadata of a LIST object
        """

        self.data_format, self.items, self.ordering, self.list_type = unpack('>4H', self.val[ : 8])


    def device(self):
        """
        Metadata of a DEVICE object
        """

        self.data_format, self.acquseq, self.items, self.dev_type = unpack('>4H', self.val[:8])
        self.dev_addr, self.n_chan  = unpack('>2I', self.val[ 8: 16])
        self.task    , self.dev_num = unpack('>2H', self.val[16: 20])
        self.n_steps                = unpack('>I' , self.val[20: 24])[0]  


    def parmset(self):
        """
        Metadata of a ParameterSet object
        """

        self.items, self.cal_type = unpack('>2H', self.val[4: 8])


    def mapping(self):
        """
        Metadata of a MAP object
        """

        self.items, self.map_type = unpack('>2H' , self.val[4: 8])
        self.task = unpack('>H' , self.val[16: 18])[0]


    def sig(self):
        """
        Metadata of a Signal or SignalGroup object
        """

        self.data_format, phys_unit, self.num_dims = unpack('>3H' , self.val[: 6])
        self.phys_unit = sfdics.unit_d[phys_unit]
        self.stat_ext = unpack('>h' , self.val[6: 8])[0]
        self.index    = unpack('>4I', self.val[8: 24])


    def tbase(self):
        """
        Metadata of a TIMEBASE object
        """

        self.data_format, self.burstcount, self.event, self.tbase_type = unpack('>4H', self.val[: 8])
        self.s_rate = unpack('>I', self.val[ 8: 12])[0] #Hz
        self.n_pre, self.n_steps = unpack('>2I', self.val[16: 24])


    def sf_list(self):
        """
        Metadata of a SF_LIST object
        """

        self.items = unpack('>H', self.val[2: 4])


    def algorithm(self):
        """
        Metadata of an ALGORITHM object
        """

        self.hostname = self.val[ 8: 16]
        self.date     = self.val[16: 24] 


    def update_set(self):
        """
        Metadata of an UPDATE_SET object
        """

        self.items =  unpack('>H' , self.val[ 2: 4])[0]
        self.input_vals = unpack('>i' , self.val[ 4: 6])[0]
        self.next_index, self.size = unpack('>I' , self.val[ 16: 24])


    def loctimer(self):
        """
        Metadata of an LOCTIMER object
        """

        self.data_format, self.resolution = unpack('>2H', self.val[: 4])
        self.size = unpack('>I', self.val[20: 24])[0]


    def abase(self):
        """
        Metadata of an AREABASE object
        """

        self.data_format = unpack('>H' , self.val[ : 2])[0]
        phys_unit   = unpack('>3H', self.val[2: 8])
        self.phys_unit = [sfdics.unit_d[x] for x in phys_unit]
        self.size_x, self.size_y, self.size_z, self.n_steps = unpack('>4I' , self.val[8: 24])


    def qualifier(self):
        """
        Metadata of an QUALIFIER object
        """

        self.data_format = unpack('>H' , self.val[ : 2])[0]
        self.num_dims, self.qsub_typ = unpack('>2H' , self.val[4: 8])
        self.index_4, self.index_3, self.index_2, self.max_sections = unpack('>4I' , self.val[8: 24])


    def addrlen(self):
        """
        Value of ADDRLEN object
        """

        self.addrlen = unpack('>H' , self.val[ : 2])[0]
