# Getting main wurp function.
from .compute import wurp

# Writer
from .parser.writer import Writer as TrjWriter

import parallel
if parallel.use_mpi:
    ParallelProcessor = parallel.ParallelProcessor
else:
    ParallelProcessor = parallel.SequentialProcessor

# Topology
from .parser import get_tplprm_simple as get_tpl

# Trajectory
from .script.conv_trj import gen_trj

# Get all the nice scripts
from . import script
