import numpy
import f2py_jit
from .helpers import _merge_source


class NeighborList(object):

    def __init__(self, rcut, neighbors='neighbor_list.f90',
                 helpers='helpers.f90', inline=True):
        self.rcut = numpy.array(rcut)
        self.neighbors = None
        self.number_neighbors = None
        self._module_path = None

        # Gather f90 sources into a single one
        source = _merge_source(helpers, neighbors)

        # Inline subroutine
        if inline:
            from f2py_jit.finline import inline_source
            source = inline_source(source, ignore='compute')  # avoid reinlining forces!

        # Compile and bundle the module with f2py
        # Build a unique module.
        # Every model with its own parameter combination corresponds to a unique module
        # and can be safely reused (up to changes in interaction / helpers)
        extra_args = '--opt="-O3 -ffast-math"'
        uid = f2py_jit.build_module(source,
                                    metadata={"neighbors": neighbors,
                                              "helpers": helpers},
                                    extra_args=extra_args,
                                    db_file='.atooms_jit.json')

        # Store module name (better not store the module itself, else we cannot deepcopy)
        self._uid = uid

    def _setup(self, npart, nneigh):
        """Allocate or reallocate arrays for neighbor list"""
        if self.neighbors is None or self.neighbors.shape[1] != npart or self.neighbors.shape[0] < nneigh:
            self.neighbors = numpy.ndarray(shape=(nneigh, npart), order='F', dtype=numpy.int32)
        if self.number_neighbors is None or len(self.number_neighbors) != npart:
            self.number_neighbors = numpy.ndarray(npart, order='F', dtype=numpy.int32)

    def compute(self, box, pos, ids):
        # Setup
        f90 = f2py_jit.import_module(self._uid)

        # Setup arrays
        # Estimate max number of neighbors based on average density
        # We take the largest cut off distance
        npart = pos.shape[1]
        rho = npart / box.prod()
        nneigh = int(4.0 / 3.0 * 3.1415 * rho * numpy.max(self.rcut)**3 * 1.50)
        self._setup(npart, nneigh)
        # Compute neighbors list
        #
        # If the f90 code returns an error, the arrays are reallocated
        # based on the largest number of neighbors returned by the f90
        # routine
        error = f90.neighbor_list.compute(box, pos, ids, self.rcut, self.neighbors, self.number_neighbors)
        if error:
            self._setup(npart, max(self.number_neighbors))
            error = f90.neighbor_list.compute(box, pos, ids, self.rcut, self.neighbors, self.number_neighbors)
            assert not error, "something wrong with neighbor_list"
