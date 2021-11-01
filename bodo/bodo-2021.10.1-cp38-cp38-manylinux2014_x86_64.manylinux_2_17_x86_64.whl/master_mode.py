import gc
import inspect
import sys
import types as pytypes
import bodo
master_mode_on = False
MASTER_RANK = 0


class MasterModeDispatcher(object):

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def __call__(self, *args, **kwargs):
        assert bodo.get_rank() == MASTER_RANK
        return master_wrapper(self.dispatcher, *args, **kwargs)

    def __getstate__(self):
        assert bodo.get_rank() == MASTER_RANK
        return self.dispatcher.py_func

    def __setstate__(self, state):
        assert bodo.get_rank() != MASTER_RANK
        obwsp__dxawd = state
        skav__apyt = inspect.getsourcelines(obwsp__dxawd)[0][0]
        assert skav__apyt.startswith('@bodo.jit') or skav__apyt.startswith(
            '@jit')
        lsxb__ghmg = eval(skav__apyt[1:])
        self.dispatcher = lsxb__ghmg(obwsp__dxawd)


def worker_loop():
    assert bodo.get_rank() != MASTER_RANK
    ale__dftz = MPI.COMM_WORLD
    while True:
        ewbld__izc = ale__dftz.bcast(None, root=MASTER_RANK)
        if ewbld__izc[0] == 'exec':
            obwsp__dxawd = pickle.loads(ewbld__izc[1])
            for epe__outwl, tzz__spvrs in list(obwsp__dxawd.__globals__.items()
                ):
                if isinstance(tzz__spvrs, MasterModeDispatcher):
                    obwsp__dxawd.__globals__[epe__outwl
                        ] = tzz__spvrs.dispatcher
            if obwsp__dxawd.__module__ not in sys.modules:
                sys.modules[obwsp__dxawd.__module__] = pytypes.ModuleType(
                    obwsp__dxawd.__module__)
            skav__apyt = inspect.getsourcelines(obwsp__dxawd)[0][0]
            assert skav__apyt.startswith('@bodo.jit') or skav__apyt.startswith(
                '@jit')
            lsxb__ghmg = eval(skav__apyt[1:])
            func = lsxb__ghmg(obwsp__dxawd)
            rgcx__fpz = ewbld__izc[2]
            nunc__ocs = ewbld__izc[3]
            vzwew__afn = []
            for jjn__gyg in rgcx__fpz:
                if jjn__gyg == 'scatter':
                    vzwew__afn.append(bodo.scatterv(None))
                elif jjn__gyg == 'bcast':
                    vzwew__afn.append(ale__dftz.bcast(None, root=MASTER_RANK))
            zezfr__ziwja = {}
            for argname, jjn__gyg in nunc__ocs.items():
                if jjn__gyg == 'scatter':
                    zezfr__ziwja[argname] = bodo.scatterv(None)
                elif jjn__gyg == 'bcast':
                    zezfr__ziwja[argname] = ale__dftz.bcast(None, root=
                        MASTER_RANK)
            hwx__mivop = func(*vzwew__afn, **zezfr__ziwja)
            if hwx__mivop is not None and func.overloads[func.signatures[0]
                ].metadata['is_return_distributed']:
                bodo.gatherv(hwx__mivop)
            del (ewbld__izc, obwsp__dxawd, func, lsxb__ghmg, rgcx__fpz,
                nunc__ocs, vzwew__afn, zezfr__ziwja, hwx__mivop)
            gc.collect()
        elif ewbld__izc[0] == 'exit':
            exit()
    assert False


def master_wrapper(func, *args, **kwargs):
    ale__dftz = MPI.COMM_WORLD
    if {'all_args_distributed', 'all_args_distributed_block',
        'all_args_distributed_varlength'} & set(func.targetoptions.keys()):
        rgcx__fpz = ['scatter' for ywjwf__taku in range(len(args))]
        nunc__ocs = {argname: 'scatter' for argname in kwargs.keys()}
    else:
        pedx__kjykk = func.py_func.__code__.co_varnames
        xwry__xrr = func.targetoptions

        def get_distribution(argname):
            if argname in xwry__xrr.get('distributed', []
                ) or argname in xwry__xrr.get('distributed_block', []):
                return 'scatter'
            else:
                return 'bcast'
        rgcx__fpz = [get_distribution(argname) for argname in pedx__kjykk[:
            len(args)]]
        nunc__ocs = {argname: get_distribution(argname) for argname in
            kwargs.keys()}
    pvzk__dcvc = pickle.dumps(func.py_func)
    ale__dftz.bcast(['exec', pvzk__dcvc, rgcx__fpz, nunc__ocs])
    vzwew__afn = []
    for nmtk__ajj, jjn__gyg in zip(args, rgcx__fpz):
        if jjn__gyg == 'scatter':
            vzwew__afn.append(bodo.scatterv(nmtk__ajj))
        elif jjn__gyg == 'bcast':
            ale__dftz.bcast(nmtk__ajj)
            vzwew__afn.append(nmtk__ajj)
    zezfr__ziwja = {}
    for argname, nmtk__ajj in kwargs.items():
        jjn__gyg = nunc__ocs[argname]
        if jjn__gyg == 'scatter':
            zezfr__ziwja[argname] = bodo.scatterv(nmtk__ajj)
        elif jjn__gyg == 'bcast':
            ale__dftz.bcast(nmtk__ajj)
            zezfr__ziwja[argname] = nmtk__ajj
    waz__hrs = []
    for epe__outwl, tzz__spvrs in list(func.py_func.__globals__.items()):
        if isinstance(tzz__spvrs, MasterModeDispatcher):
            waz__hrs.append((func.py_func.__globals__, epe__outwl, func.
                py_func.__globals__[epe__outwl]))
            func.py_func.__globals__[epe__outwl] = tzz__spvrs.dispatcher
    hwx__mivop = func(*vzwew__afn, **zezfr__ziwja)
    for edjxt__mpwom, epe__outwl, tzz__spvrs in waz__hrs:
        edjxt__mpwom[epe__outwl] = tzz__spvrs
    if hwx__mivop is not None and func.overloads[func.signatures[0]].metadata[
        'is_return_distributed']:
        hwx__mivop = bodo.gatherv(hwx__mivop)
    return hwx__mivop


def init_master_mode():
    if bodo.get_size() == 1:
        return
    global master_mode_on
    assert master_mode_on is False, 'init_master_mode can only be called once on each process'
    master_mode_on = True
    assert sys.version_info[:2] >= (3, 8
        ), 'Python 3.8+ required for master mode'
    from bodo import jit
    globals()['jit'] = jit
    import cloudpickle
    from mpi4py import MPI
    globals()['pickle'] = cloudpickle
    globals()['MPI'] = MPI

    def master_exit():
        MPI.COMM_WORLD.bcast(['exit'])
    if bodo.get_rank() == MASTER_RANK:
        import atexit
        atexit.register(master_exit)
    else:
        worker_loop()
