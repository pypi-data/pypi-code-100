"""Support distributed deep learning with Horovod
"""
import time
import numba
import numpy as np
from mpi4py import MPI
import bodo
from bodo.libs.distributed_api import create_subcomm_mpi4py, get_host_ranks, get_nodes_first_ranks
dl_status = None


def assert_dl_initialized():
    assert dl_status is not None, 'Horovod has not been initialized. Call bodo.dl.start() first'


class DLStatus(object):

    def __init__(self, framework, gpu_ranks):
        self.framework = framework
        self.gpu_ranks = gpu_ranks


def get_num_gpus(framework):
    if framework == 'torch':
        import torch
        return torch.cuda.device_count()
    elif framework == 'tensorflow':
        import tensorflow as tf
        return len(tf.config.experimental.list_physical_devices('GPU'))
    else:
        raise RuntimeError('Framework {} not recognized'.format(framework))


def get_gpu_ranks(framework):
    jfo__zifj = MPI.COMM_WORLD
    prru__fdho = jfo__zifj.Get_rank()
    cgf__wdati = get_host_ranks()
    lfv__husiw = get_nodes_first_ranks()
    if prru__fdho in lfv__husiw:
        try:
            cwpja__qmdv = get_num_gpus(framework)
        except Exception as vbyyw__thsrw:
            cwpja__qmdv = vbyyw__thsrw
        sqpuw__bekx = create_subcomm_mpi4py(lfv__husiw)
        tae__xzzz = sqpuw__bekx.gather(cwpja__qmdv)
        if prru__fdho == 0:
            gpu_ranks = []
            itt__pgls = None
            for jnpxj__eam, qlgq__lhn in enumerate(cgf__wdati.values()):
                rwnqx__gbot = tae__xzzz[jnpxj__eam]
                if isinstance(rwnqx__gbot, Exception):
                    itt__pgls = rwnqx__gbot
                    break
                if rwnqx__gbot == 0:
                    continue
                ure__vpxl = len(qlgq__lhn) // rwnqx__gbot
                for yfsx__ven, kreq__rcd in enumerate(qlgq__lhn):
                    if yfsx__ven % ure__vpxl == 0:
                        cszlv__fpzup = yfsx__ven / ure__vpxl
                        if cszlv__fpzup < rwnqx__gbot:
                            gpu_ranks.append(kreq__rcd)
            if itt__pgls:
                jfo__zifj.bcast(itt__pgls)
                raise itt__pgls
            else:
                jfo__zifj.bcast(gpu_ranks)
    if prru__fdho != 0:
        gpu_ranks = jfo__zifj.bcast(None)
        if isinstance(gpu_ranks, Exception):
            vbyyw__thsrw = gpu_ranks
            raise vbyyw__thsrw
    return gpu_ranks


def is_cuda_available():
    assert_dl_initialized()
    return len(dl_status.gpu_ranks) > 0


def initialize_horovod(framework):
    global dl_status
    if dl_status is not None:
        assert dl_status.framework == framework, 'Attempted to initialize Horovod with different DL frameworks'
        return np.array(dl_status.gpu_ranks, dtype=np.int32)
    gpu_ranks = get_gpu_ranks(framework)
    if framework == 'torch':
        import horovod.torch as hvd
        import torch
        torch.set_num_threads(1)
    elif framework == 'tensorflow':
        import horovod.tensorflow as hvd
        import tensorflow as tf
    else:
        raise RuntimeError('Framework {} not recognized'.format(framework))
    gdscd__ovrrz = MPI.COMM_WORLD.rank
    if len(gpu_ranks) > 0:
        sqpuw__bekx = MPI.COMM_WORLD.Split(color=0 if gdscd__ovrrz in
            gpu_ranks else MPI.UNDEFINED, key=gdscd__ovrrz)
        if sqpuw__bekx != MPI.COMM_NULL:
            hvd.init(comm=sqpuw__bekx)
            if framework == 'torch':
                torch.cuda.set_device(hvd.local_rank())
            elif framework == 'tensorflow':
                gzxv__iptkd = tf.config.experimental.list_physical_devices(
                    'GPU')
                for xamas__dxa in gzxv__iptkd:
                    tf.config.experimental.set_memory_growth(xamas__dxa, True)
                tf.config.experimental.set_visible_devices(gzxv__iptkd[hvd.
                    local_rank()], 'GPU')
    else:
        if gdscd__ovrrz == 0:
            print('[BODO-DL]: No GPUs found in cluster. Using CPUs')
        hvd.init()
    dl_status = DLStatus(framework, np.array(gpu_ranks, dtype=np.int32))


@numba.njit
def start(framework):
    with numba.objmode:
        initialize_horovod(framework)


@numba.njit
def end():
    with numba.objmode:
        end_py()


def end_py():
    if is_cuda_available():
        rrd__omn = 17
        jfo__zifj = MPI.COMM_WORLD
        sts__tyq = MPI.Get_processor_name()
        cximv__dymd = get_host_ranks()[sts__tyq]
        assert_dl_initialized()
        if bodo.get_rank() == cximv__dymd[0]:
            assert bodo.get_rank() in dl_status.gpu_ranks
            for prru__fdho in cximv__dymd[1:]:
                jfo__zifj.isend(1, dest=prru__fdho, tag=rrd__omn)
        else:
            while True:
                jdt__rplp = MPI.Status()
                qrqoa__rjjq = jfo__zifj.Iprobe(MPI.ANY_SOURCE, MPI.ANY_TAG,
                    jdt__rplp)
                if qrqoa__rjjq:
                    assert jdt__rplp.source == cximv__dymd[0]
                    assert jdt__rplp.tag == rrd__omn
                    jfo__zifj.recv(source=0, tag=rrd__omn)
                    break
                time.sleep(1.0)
    else:
        bodo.barrier()


def _prepare_data_get_gpu_ranks():
    assert_dl_initialized()
    return dl_status.gpu_ranks


@numba.njit
def prepare_data(data):
    with numba.objmode(gpu_ranks='int32[:]'):
        gpu_ranks = _prepare_data_get_gpu_ranks()
    if len(gpu_ranks) > 0:
        data = bodo.rebalance(data, dests=list(gpu_ranks), parallel=True)
    else:
        data = bodo.rebalance(data, parallel=True)
    return data
