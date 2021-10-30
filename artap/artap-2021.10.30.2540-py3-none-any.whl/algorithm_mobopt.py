from .problem import Problem
from .algorithm import Algorithm
from .individual import Individual

import time
import array
import random

# -*- coding: utf-8 -*-

import numpy as np

from sklearn.gaussian_process import GaussianProcessRegressor as GPR
from sklearn.gaussian_process.kernels import Matern

from scipy.spatial.distance import directed_hausdorff as HD

# from .metrics import GD, Spread2D, Coverage


from deap import base
from deap import creator
from deap import tools

FirstCall = True


def uniform(bounds):
    return [random.uniform(b[0], b[1]) for b in bounds]


def NSGAII(NObj, objective, pbounds, seed=None, NGEN=100, MU=100, CXPB=0.9):
    random.seed(seed)

    global FirstCall
    if FirstCall:
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,) * NObj)
        creator.create("Individual", array.array, typecode='d',
                       fitness=creator.FitnessMin)
        FirstCall = False
    toolbox = base.Toolbox()

    NDIM = len(pbounds)

    toolbox.register("attr_float", uniform, pbounds)

    toolbox.register("individual",
                     tools.initIterate,
                     creator.Individual,
                     toolbox.attr_float)

    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", objective)

    toolbox.register("mate",
                     tools.cxSimulatedBinaryBounded,
                     low=pbounds[:, 0].tolist(),
                     up=pbounds[:, 1].tolist(),
                     eta=20.0)

    toolbox.register("mutate",
                     tools.mutPolynomialBounded,
                     low=pbounds[:, 0].tolist(),
                     up=pbounds[:, 1].tolist(),
                     eta=20.0,
                     indpb=1.0 / NDIM)

    toolbox.register("select", tools.selNSGA2)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)

    logbook = tools.Logbook()
    logbook.header = "gen", "evals", "std", "min", "avg", "max"

    pop = toolbox.population(n=MU)

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    # This is just to assign the crowding distance to the individuals
    # no actual selection is done
    pop = toolbox.select(pop, len(pop))

    record = stats.compile(pop)
    logbook.record(gen=0, evals=len(invalid_ind), **record)

    # Begin the generational process
    for gen in range(1, NGEN):
        # Vary the population
        offspring = tools.selTournamentDCD(pop, len(pop))
        offspring = [toolbox.clone(ind) for ind in offspring]

        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            if random.random() <= CXPB:
                toolbox.mate(ind1, ind2)

            toolbox.mutate(ind1)
            toolbox.mutate(ind2)
            del ind1.fitness.values, ind2.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Select the next generation population
        pop = toolbox.select(pop + offspring, MU)
        record = stats.compile(pop)
        logbook.record(gen=gen, evals=len(invalid_ind), **record)
        # print(logbook.stream)

    front = np.array([ind.fitness.values for ind in pop])

    return pop, logbook, front


def hypervolume(pointset, ref):
    """Compute the absolute hypervolume of a *pointset* according to the
    reference point *ref*.
    """
    hv = _HyperVolume(ref)
    return hv.compute(pointset)


class _HyperVolume:
    """
    Hypervolume computation based on variant 3 of the algorithm in the paper:
    C. M. Fonseca, L. Paquete, and M. Lopez-Ibanez. An improved dimension-sweep
    algorithm for the hypervolume indicator. In IEEE Congress on Evolutionary
    Computation, pages 1157-1163, Vancouver, Canada, July 2006.
    Minimization is implicitly assumed here!
    """

    def __init__(self, referencePoint):
        """Constructor."""
        self.referencePoint = referencePoint
        self.list = []

    def compute(self, front):
        """Returns the hypervolume that is dominated by a non-dominated front.
        Before the HV computation, front and reference point are translated, so
        that the reference point is [0, ..., 0].
        """

        def weaklyDominates(point, other):
            for i in range(len(point)):
                if point[i] > other[i]:
                    return False
            return True

        relevantPoints = []
        referencePoint = self.referencePoint
        dimensions = len(referencePoint)
        #######
        # fmder: Here it is assumed that every point dominates the reference point
        # for point in front:
        #     # only consider points that dominate the reference point
        #     if weaklyDominates(point, referencePoint):
        #         relevantPoints.append(point)
        relevantPoints = front
        # fmder
        #######
        if any(referencePoint):
            # shift points so that referencePoint == [0, ..., 0]
            # this way the reference point doesn't have to be explicitly used
            # in the HV computation

            #######
            # fmder: Assume relevantPoints are numpy array
            # for j in xrange(len(relevantPoints)):
            #     relevantPoints[j] = [relevantPoints[j][i] - referencePoint[i] for i in xrange(dimensions)]
            relevantPoints -= referencePoint
            # fmder
            #######

        self.preProcess(relevantPoints)
        bounds = [-1.0e308] * dimensions
        hyperVolume = self.hvRecursive(dimensions - 1, len(relevantPoints), bounds)
        return hyperVolume

    def hvRecursive(self, dimIndex, length, bounds):
        """Recursive call to hypervolume calculation.
        In contrast to the paper, the code assumes that the reference point
        is [0, ..., 0]. This allows the avoidance of a few operations.
        """
        hvol = 0.0
        sentinel = self.list.sentinel
        if length == 0:
            return hvol
        elif dimIndex == 0:
            # special case: only one dimension
            # why using hypervolume at all?
            return -sentinel.next[0].cargo[0]
        elif dimIndex == 1:
            # special case: two dimensions, end recursion
            q = sentinel.next[1]
            h = q.cargo[0]
            p = q.next[1]
            while p is not sentinel:
                pCargo = p.cargo
                hvol += h * (q.cargo[1] - pCargo[1])
                if pCargo[0] < h:
                    h = pCargo[0]
                q = p
                p = q.next[1]
            hvol += h * q.cargo[1]
            return hvol
        else:
            remove = self.list.remove
            reinsert = self.list.reinsert
            hvRecursive = self.hvRecursive
            p = sentinel
            q = p.prev[dimIndex]
            while q.cargo != None:
                if q.ignore < dimIndex:
                    q.ignore = 0
                q = q.prev[dimIndex]
            q = p.prev[dimIndex]
            while length > 1 and (q.cargo[dimIndex] > bounds[dimIndex] or q.prev[dimIndex].cargo[dimIndex] >= bounds[dimIndex]):
                p = q
                remove(p, dimIndex, bounds)
                q = p.prev[dimIndex]
                length -= 1
            qArea = q.area
            qCargo = q.cargo
            qPrevDimIndex = q.prev[dimIndex]
            if length > 1:
                hvol = qPrevDimIndex.volume[dimIndex] + qPrevDimIndex.area[dimIndex] * (qCargo[dimIndex] - qPrevDimIndex.cargo[dimIndex])
            else:
                qArea[0] = 1
                qArea[1:dimIndex + 1] = [qArea[i] * -qCargo[i] for i in range(dimIndex)]
            q.volume[dimIndex] = hvol
            if q.ignore >= dimIndex:
                qArea[dimIndex] = qPrevDimIndex.area[dimIndex]
            else:
                qArea[dimIndex] = hvRecursive(dimIndex - 1, length, bounds)
                if qArea[dimIndex] <= qPrevDimIndex.area[dimIndex]:
                    q.ignore = dimIndex
            while p is not sentinel:
                pCargoDimIndex = p.cargo[dimIndex]
                hvol += q.area[dimIndex] * (pCargoDimIndex - q.cargo[dimIndex])
                bounds[dimIndex] = pCargoDimIndex
                reinsert(p, dimIndex, bounds)
                length += 1
                q = p
                p = p.next[dimIndex]
                q.volume[dimIndex] = hvol
                if q.ignore >= dimIndex:
                    q.area[dimIndex] = q.prev[dimIndex].area[dimIndex]
                else:
                    q.area[dimIndex] = hvRecursive(dimIndex - 1, length, bounds)
                    if q.area[dimIndex] <= q.prev[dimIndex].area[dimIndex]:
                        q.ignore = dimIndex
            hvol -= q.area[dimIndex] * q.cargo[dimIndex]
            return hvol

    def preProcess(self, front):
        """Sets up the list data structure needed for calculation."""
        dimensions = len(self.referencePoint)
        nodeList = _MultiList(dimensions)
        nodes = [_MultiList.Node(dimensions, point) for point in front]
        for i in range(dimensions):
            self.sortByDimension(nodes, i)
            nodeList.extend(nodes, i)
        self.list = nodeList

    def sortByDimension(self, nodes, i):
        """Sorts the list of nodes by the i-th value of the contained points."""
        # build a list of tuples of (point[i], node)
        decorated = [(node.cargo[i], node) for node in nodes]
        # sort by this value
        decorated.sort()
        # write back to original list
        nodes[:] = [node for (_, node) in decorated]


class _MultiList:
    """A special data structure needed by FonsecaHyperVolume.

    It consists of several doubly linked lists that share common nodes. So,
    every node has multiple predecessors and successors, one in every list.
    """

    class Node:

        def __init__(self, numberLists, cargo=None):
            self.cargo = cargo
            self.next = [None] * numberLists
            self.prev = [None] * numberLists
            self.ignore = 0
            self.area = [0.0] * numberLists
            self.volume = [0.0] * numberLists

        def __str__(self):
            return str(self.cargo)

        def __lt__(self, other):
            return all(self.cargo < other.cargo)

    def __init__(self, numberLists):
        """Constructor.

        Builds 'numberLists' doubly linked lists.
        """
        self.numberLists = numberLists
        self.sentinel = _MultiList.Node(numberLists)
        self.sentinel.next = [self.sentinel] * numberLists
        self.sentinel.prev = [self.sentinel] * numberLists

    def __str__(self):
        strings = []
        for i in range(self.numberLists):
            currentList = []
            node = self.sentinel.next[i]
            while node != self.sentinel:
                currentList.append(str(node))
                node = node.next[i]
            strings.append(str(currentList))
        stringRepr = ""
        for string in strings:
            stringRepr += string + "\n"
        return stringRepr

    def __len__(self):
        """Returns the number of lists that are included in this _MultiList."""
        return self.numberLists

    def getLength(self, i):
        """Returns the length of the i-th list."""
        length = 0
        sentinel = self.sentinel
        node = sentinel.next[i]
        while node != sentinel:
            length += 1
            node = node.next[i]
        return length

    def append(self, node, index):
        """Appends a node to the end of the list at the given index."""
        lastButOne = self.sentinel.prev[index]
        node.next[index] = self.sentinel
        node.prev[index] = lastButOne
        # set the last element as the new one
        self.sentinel.prev[index] = node
        lastButOne.next[index] = node

    def extend(self, nodes, index):
        """Extends the list at the given index with the nodes."""
        sentinel = self.sentinel
        for node in nodes:
            lastButOne = sentinel.prev[index]
            node.next[index] = sentinel
            node.prev[index] = lastButOne
            # set the last element as the new one
            sentinel.prev[index] = node
            lastButOne.next[index] = node

    def remove(self, node, index, bounds):
        """Removes and returns 'node' from all lists in [0, 'index'[."""
        for i in range(index):
            predecessor = node.prev[i]
            successor = node.next[i]
            predecessor.next[i] = successor
            successor.prev[i] = predecessor
            if bounds[i] > node.cargo[i]:
                bounds[i] = node.cargo[i]
        return node

    def reinsert(self, node, index, bounds):
        """
        Inserts 'node' at the position it had in all lists in [0, 'index'[
        before it was removed. This method assumes that the next and previous
        nodes of the node that is reinserted are in the list.
        """
        for i in range(index):
            node.prev[i].next[i] = node
            node.next[i].prev[i] = node
            if bounds[i] > node.cargo[i]:
                bounds[i] = node.cargo[i]


class TargetSpace(object):
    """
    Holds the param-space coordinates (X) and target values (Y)
    """

    def __init__(self, target_function, NObj, pbounds, constraints,
                 RandomSeed, init_points=2, verbose=False):
        """
        Keyword Arguments:
        target_function -- list of Functions to be maximized
        NObj            -- Number of objective functions
        pbounds         -- numpy array with bounds for each parameter
        """

        super(TargetSpace, self).__init__()

        self.vprint = print if verbose else lambda *a, **k: None

        self.RS = np.random.RandomState(seed=RandomSeed)

        self.target_function = target_function
        self.NObj = NObj

        self.ParetoSize = 0

        self.pbounds = pbounds
        self.constraints = constraints
        self.init_points = init_points

        if len(self.constraints) == 0:
            self.__NoConstraint = True

        # Find number of parameters
        self.NParam = self.pbounds.shape[0]

        self.q = self.NParam
        # Number of observations
        self._NObs = 0

        self._X = None
        self._Y = None  # binary result for dominance
        self._W = None  # binary result for dominance
        self._F = None  # result of the target functions
        self.length = 0

        return

    # % Satisfy constraints
    def SatisfyConstraints(self, x, tol=1.0e-6):
        for cons in self.constraints:
            y = cons['fun'](x)
            if cons['type'] == 'eq':
                if np.abs(y) > tol:
                    return False
            elif cons['type'] == 'ineq':
                if y < -tol:
                    return False
        return True

    # % Other
    @property
    def X(self):
        return self._X

    @property
    def Y(self):
        return self._Y

    @property
    def W(self):
        return self._W

    @property
    def x(self):
        return self.X[:self.length]

    @property
    def y(self):
        return self.Y[:self.length]

    @property
    def f(self):
        return self._F[:self.length]

    @property
    def w(self):
        return self.W[:self.length]

    @property
    def _n_alloc_rows(self):
        """ Number of allocated rows """
        return 0 if self._X is None else self._X.shape[0]

    def __len__(self):
        return self.length

    # % CONTAINS
    def __contains__(self, x):
        try:
            return x in self._X
        except:  # noqa
            return False

    def __repr__(self):
        HeaderX = ''.join(f'   X{i}    ' for i in range(self.NParam))
        HeaderY = ''.join(f'   F{i}    ' for i in range(self.NObj))
        Out = HeaderX + ' | ' + HeaderY + '\n'
        for i in range(self.length):
            LineX = ''.join(f'{i:+3.1e} ' for i in self.x[i])
            LineY = ''.join(f'{i:+3.1e} ' for i in self.f[i])
            Out += LineX + ' | ' + LineY + '\n'
        return Out

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.x[key], self.f[key]
        elif isinstance(key, int):
            if key < self.length:
                return self.x[key], self.f[key]
            else:
                raise KeyError(f"key ({key}) larger than {self.length}")
        else:
            raise TypeError(f"Invalid key type for space")

    # % RANDOM POINTS
    def random_points(self, num):
        """
        Creates random points within the bounds of the space
        Keyword Arguments:
        num  -- number of random points to create
        Returns:
        data -- [num x NParam] array of points
        """

        data = np.empty((num, self.NParam))

        for i in enumerate(data):
            while True:
                DD = self.OneRandomPoint(self.NParam, self.pbounds, self.RS)
                if self.SatisfyConstraints(DD):
                    data[i[0]] = DD
                    break
        return data.tolist()

    # % return one point
    @staticmethod
    def OneRandomPoint(NParam, pbounds, RS):
        x = np.empty(NParam)
        counter = 0
        for b in pbounds:
            if b[0] is None and b[1] is None:
                x[counter] = RS.normal(size=1)
            elif b[0] is None:
                x[counter] = b[1] - RS.exponential(size=1)
            elif b[1] is None:
                x[counter] = b[0] + RS.exponential(size=1)
            else:
                x[counter] = RS.uniform(low=b[0], high=b[1], size=1)
            counter += 1
        return x.tolist()

    # % OBSERVE POINT
    def observe_point(self, x):
        """
        Evaluates a single point x, to obtain the value y and them records
        them as observations
        NOTE: if x has been previously seen returns a cached value of y
        Keyword Arguments:
        x    -- a single point, w/ len(x) == self.NParam
        """

        assert x.size == self.NParam, 'x must have the same dimension'

        f = self.target_function(x)

        try:
            NewF = []
            for ff in f:
                NewF.append(ff[0])
            f = NewF
        except:  # noqa
            pass

        self.add_observation(x, f)

        return f

    # % ADD POINT
    def add_observation(self, x, f):
        """
        Append a point and its target values to the known data
        Keyword Arguments:
        x    -- a single point
        y    --  target function value
        """

        assert x.size == self.NParam, 'x must have the same dimension'

        if self.length >= self._n_alloc_rows:
            self._allocate((self.length + 1) * 2)

        self._X[self.length] = x
        self._F[self.length] = f
        self._Y[self.length] = self.dominated(f)

        self.length += 1
        self.UpdateDominance()
        # self.DominanceWeight()

        self.ParetoSize = len(np.where(self._Y == 1)[0])

        return

    # % Pareto Set
    def ParetoSet(self):
        iPareto = np.where(self._Y == 1)[0]
        return self._F[iPareto], self._X[iPareto]

    # % Update dominance
    def UpdateDominance(self):
        for i in range(self.length - 1):
            if self._Y[i] == 1:
                if self.Larger(self._F[self.length - 1], self._F[i]):
                    self._Y[i] = 0
        return

    def DominanceWeight(self):
        for i in range(self.length):
            self.w[i] = 0
            for j in range(self.length):
                if i != j:
                    if self.Larger(self._F[j], self._F[i]):
                        self.w[i] += 1
            self.w[i] = np.exp(-self.w[i])
        return

    # % test for dominance
    def dominated(self, f):
        # returns 1 if non-dominated 0 if dominated
        Dominated = 1
        for i in range(self.length):
            if self._Y[i] == 1:
                if self.Larger(self._F[i], f):
                    Dominated = 0
                    break
        return Dominated

    # % Compare two lists
    @staticmethod
    def Larger(X, Y):
        # test if X > Y
        Dominates = True
        NumberOfLarger = 0
        for i, x in enumerate(X):
            if x > Y[i]:
                Dominates = Dominates and True
                NumberOfLarger += 1
            elif x == Y[i]:
                Dominates = Dominates and True
            else:
                Dominates = Dominates and False
                break
        Dominates = Dominates and (NumberOfLarger > 0)
        return Dominates

    # % allocate memory

    def _allocate(self, num):
        """
        Keyword Arguments:
        num  -- number of points to be allocated
        """

        if num <= self._n_alloc_rows:
            raise ValueError('num must be larger than current array length')

        #  Allocate new memory
        _Xnew = np.empty((num, self.NParam))
        _Ynew = np.empty(num, dtype=object)
        _Wnew = np.empty(num, dtype=object)
        _Fnew = np.empty((num, self.NObj))
        # _Fnew = np.empty(num,dtype=object)
        # Copy the old data into the new
        if self._X is not None:
            _Xnew[:self.length] = self._X[:self.length]
            _Ynew[:self.length] = self._Y[:self.length]
            _Wnew[:self.length] = self._W[:self.length]
            _Fnew[:self.length] = self._F[:self.length]

        self._X = _Xnew
        self._Y = _Ynew
        self._W = _Wnew
        self._F = _Fnew

        return


class ConstraintError(Exception):
    pass


class MOBayesian(Algorithm):
    def __init__(self, problem, name="Multiobjective Bayesians Optimization"):
        super().__init__(problem, name)

    def _target(self, x):
        individual = Individual(x)
        self.evaluator.evaluate([individual])
        self.problem.individuals.append(individual)

        print("x = {}, f_1 = {}".format(x, individual.costs[0]))
        return individual.costs

    def run(self):
        pbounds = []
        for parameter in self.problem.parameters:
            bounds = parameter['bounds']
            pbounds.append(bounds)

        # "Number of restarts of GP optimizer"
        NRest = 10

        # "Number of initialization points"
        N_init = 5

        Optimize = MOBayesianOpt(target=self._target,
                                 NObj=len(self.problem.costs),
                                 pbounds=np.array(pbounds),
                                 MetricsPS=False,
                                 verbose=self.options['verbose_level'] > 0,
                                 n_restarts_optimizer=NRest)

        Optimize.initialize(init_points=N_init)

        # "If present reduces prob linearly along simulation"
        Reduce = False
        # "Probability of random jumps"
        Prob = 1.0
        # "Weight in factor"
        Q = 1.0

        front, pop = Optimize.minimize(n_iter=self.options['n_iterations'],
                                       prob=Prob,
                                       q=Q,
                                       FrontSampling=[20],
                                       ReduceProb=Reduce)

        # print(pop)
        # sync changed individual informations
        self.problem.data_store.sync_all()

        # GenDist = mo.metrics.GD(front, np.asarray([f1, f2]).T)
        # Delta = mo.metrics.Spread2D(front, np.asarray([f1, f2]).T)


# Class Bayesians Optimization
class MOBayesianOpt(object):
    def __init__(self, target, NObj, pbounds, constraints=[],
                 verbose=False, n_restarts_optimizer=10, MetricsPS=True, max_or_min='min', RandomSeed=None):
        """Bayesian optimization object

        Keyword Arguments:
        target  -- functions to be optimized
                   def target(x): x is a np.array
                       return [f_1, f_2, ..., f_NObj]

        NObj    -- int, Number of objective functions

        pbounds -- numpy array with bounds for each parameter
                   pbounds.shape == (NParam,2)

        constraints -- list of dictionary with constraints
                   [{'type': 'ineq', 'fun': constr_fun}, ...]

                   def constr_fun(x):
                       return g(x) # >= 0

        verbose -- Whether or not to print progress (default False)

        n_restarts_optimizer -- int (default 100)
             GP parameter, the number of restarts of the optimizer for
             finding the kernel’s parameters which maximize the log-marginal
             likelihood.

        MetricsPS -- bool (default True)
             whether os not to calculate metrics with the Pareto Set points

        RandomSeed -- {None, int, array_like}, optional
            Random seed used to initialize the pseudo-random number
            generator. Can be any integer between 0 and 2**32 - 1
            inclusive, an array (or other sequence) of such integers,
            or None (the default). If seed is None, then RandomState
            will try to read data from /dev/urandom (or the Windows
            analogue) if available or seed from the clock otherwise.

        Based heavily on github.com/fmfn/BayesianOptimization

        """

        super(MOBayesianOpt, self).__init__()

        self.verbose = verbose
        self.vprint = print if verbose else lambda *a, **k: None

        self.counter = 0
        self.constraints = constraints
        self.n_rest_opt = n_restarts_optimizer
        self.MetricsPS = MetricsPS

        # reset calling variables
        self.__reset__()

        # number of objective functions
        if isinstance(NObj, int):
            self.NObj = NObj
        else:
            raise TypeError("NObj should be int")

        # objective function returns lists w/ the multiple target functions
        if callable(target):
            self.target = target
        else:
            raise TypeError("target should be callable")

        self.pbounds = pbounds
        # pbounds must hold the bounds for each parameter
        try:
            self.NParam = len(pbounds)
        except TypeError:
            raise TypeError("pbounds is neither a np.array nor a list")
        if self.pbounds.shape != (self.NParam, 2):
            raise IndexError("pbounds must have 2nd dimension equal to 2")

        self.vprint(f"Dim. of Search Space = {self.NParam}")

        self.GP = [None] * self.NObj
        for i in range(self.NObj):
            self.GP[i] = GPR(kernel=Matern(nu=1.5), n_restarts_optimizer=self.n_rest_opt)

        # store starting points
        self.init_points = []

        # test for constraint types
        for cc in self.constraints:
            if cc['type'] == 'eq':
                raise ConstraintError(
                    "Equality constraints are not implemented")

        self.space = TargetSpace(self.target, self.NObj, self.pbounds,
                                 self.constraints,
                                 RandomSeed=RandomSeed,
                                 verbose=self.verbose)

        return

    # % RESET
    def __reset__(self):
        """
        RESET all function initialization variables
        """
        self.__CalledInit = False

        return

    # % INIT
    def initialize(self, init_points=None, Points=[]):
        """
        Initialization of the method

        Keyword Arguments:
        init_points -- Number of random points to probe
        points -- list of points in which to sample the method

        At first, no points provided by the user are gonna be used by the
        algorithm, Only points calculated randomly, respecting the bounds
        provided
        """

        self.N_init_points = 0
        if init_points is not None:
            self.N_init_points += init_points

            # initialize first points for the gp fit,
            # random points respecting the bounds of the variables.
            rand_points = self.space.random_points(init_points)
            self.init_points.extend(rand_points)
            self.init_points = np.asarray(self.init_points)

            # evaluate target function at all intialization points
            for x in self.init_points:
                dummy = self.space.observe_point(x)

        if len(Points) > 0:
            for ii in range(len(Points)):
                dummy = self.space.observe_point(Points[ii])  # noqa
                self.N_init_points += 1

        if self.N_init_points == 0:
            raise RuntimeError(
                "A non-zero number of initialization points is required")

        self.vprint("Added points in init")
        self.vprint(self.space.x)

        self.__CalledInit = True

        return

    # % minimize
    def minimize(self,
                 n_iter=100,
                 prob=0.1,
                 ReduceProb=False,
                 q=0.5,
                 n_pts=100,
                 FrontSampling=[10, 25, 50, 100]):
        """
        minimize

        input
        =====

        n_iter -- int (default 100)
            number of iterations of the method

        prob -- float ( 0 < prob < 1, default 0.1
            probability of chosing next point randomly

        ReduceProb -- bool (default False)
            if True prob is reduced to zero along the iterations of the method

        q -- float ( 0 < q < 1.0, default 0.5 )
            weight between Search space and objective space when selecting next
            iteration point
            q = 1 : objective space only
            q = 0 : search space only

        n_pts -- int
            effective size of the pareto front
            (len(front = n_pts))

        FrontSampling -- list of ints
             Number of points to sample the pareto front for metrics

        return front, pop
        =================

        front -- Pareto front of the method as found by the nsga2 at the
                 last iteration of the method
        pop -- population of points in search space as found by the nsga2 at
               the last iteration of the method

        Outputs
        =======

        self.y_Pareto :: list of non-dominated points in objective space
        self.x_Pareto :: list of non-dominated points in search space
        """
        # If initialize was not called, call it and allocate necessary space
        if not self.__CalledInit:
            raise RuntimeError("Initialize was not called, "
                               "call it before calling maximize")

        if not isinstance(n_iter, int):
            raise TypeError(f"n_iter should be int, {type(n_iter)} instead")

        if not isinstance(n_pts, int):
            raise TypeError(f"n_pts should be int, "
                            f"{type(n_pts)} instead")

        if isinstance(FrontSampling, list):
            if not all([isinstance(n, int) for n in FrontSampling]):
                raise TypeError(f"FrontSampling should be list of int")
        else:
            raise TypeError(f"FrontSampling should be a list")

        if not isinstance(prob, (int, float)):
            raise TypeError(f"prob should be float, "
                            f"{type(prob)} instead")

        if not isinstance(q, (int, float)):
            raise TypeError(f"q should be float, "
                            f"{type(q)} instead")

        if not isinstance(ReduceProb, bool):
            raise TypeError(f"ReduceProb should be bool, "
                            f"{type(ReduceProb)} instead")

        # Allocate necessary space
        if self.N_init_points + n_iter > self.space._n_alloc_rows:
            self.space._allocate(self.N_init_points + n_iter)

        self.q = q
        self.NewProb = prob

        self.vprint("Start optimization loop")

        for i in range(n_iter):

            self.vprint(i, " of ", n_iter)
            if ReduceProb:
                self.NewProb = prob * (1.0 - self.counter / n_iter)

            for i in range(self.NObj):
                yy = self.space.f[:, i]
                self.GP[i].fit(self.space.x, yy)

            pop, logbook, front = NSGAII(self.NObj,
                                         self.__ObjectiveGP,
                                         self.pbounds,
                                         MU=n_pts)

            Population = np.asarray(pop)
            IndexF, FatorF = self.__LargestOfLeast(front, self.space.f)
            IndexPop, FatorPop = self.__LargestOfLeast(Population,
                                                       self.space.x)

            Fator = self.q * FatorF + (1 - self.q) * FatorPop
            Index_try = np.argmax(Fator)

            self.vprint("IF = ", IndexF,
                        " IP = ", IndexPop,
                        " Try = ", Index_try)

            self.vprint("Front at = ", -front[Index_try])

            self.x_try = Population[Index_try]

            if self.space.RS.uniform() < self.NewProb:

                if self.NParam > 1:
                    ii = self.space.RS.randint(low=0, high=self.NParam - 1)
                else:
                    ii = 0

                self.x_try[ii] = self.space.RS.uniform(
                    low=self.pbounds[ii][0],
                    high=self.pbounds[ii][1])

                self.vprint("Random Point at ", ii, " coordinate")

            dummy = self.space.observe_point(self.x_try)  # noqa

            self.y_Pareto, self.x_Pareto = self.space.ParetoSet()
            self.counter += 1

            self.vprint(f"|PF| = {self.space.ParetoSize:4d} at"
                        f" {self.counter:4d}"
                        f" of {n_iter:4d}, w/ r = {self.NewProb:4.2f}")

        return front, np.asarray(pop)

    def __LargestOfLeast(self, front, F):
        NF = len(front)
        MinDist = np.empty(NF)
        for i in range(NF):
            MinDist[i] = self.__MinimalDistance(-front[i], F)

        ArgMax = np.argmax(MinDist)

        Mean = MinDist.mean()
        Std = np.std(MinDist)
        return ArgMax, (MinDist - Mean) / (Std)

    def __PrintOutput(self, front, pop, SaveFile=False):

        NFront = front.shape[0]

        # GenDist = GD(front, self.TPF)
        # SS = Spread2D(front, self.TPF)
        # HausDist = HD(front, self.TPF)[0]

        # Cover = Coverage(front)
        Cover = 0.0
        HV = hypervolume(pop, [11.0] * self.NObj)

        if self.MetricsPS and self.Metrics:
            FPS = []
            for x in pop:
                FF = - self.target(x)
                FPS += [[FF[i] for i in range(self.NObj)]]
            FPS = np.array(FPS)

            # GDPS = GD(FPS, self.TPF)
            # SSPS = Spread2D(FPS, self.TPF)
            # HDPS = HD(FPS, self.TPF)[0]
        else:
            GDPS = np.nan
            SSPS = np.nan
            HDPS = np.nan

        self.vprint(f"NFront = {NFront} | HV = {HV:7.3e} ")

        return

    @staticmethod
    def __MinimalDistance(X, Y):
        N = len(X)
        Npts = len(Y)
        DistMin = float('inf')
        for i in range(Npts):
            Dist = 0.
            for j in range(N):
                Dist += (X[j] - Y[i, j]) ** 2
            Dist = np.sqrt(Dist)
            if Dist < DistMin:
                DistMin = Dist
        return DistMin

    def __MaxDist(self, front, yPareto):
        NF = len(front)
        IndexMax = 0
        DistMax = self.__DistTotal(-front[0], yPareto)
        for i in range(1, NF):
            Dist = self.__DistTotal(-front[i], yPareto)
            if Dist > DistMax:
                DistMax = Dist
                IndexMax = i
        return IndexMax

    @staticmethod
    def __DistTotal(X, Y):
        Soma = 0.0
        for i in range(len(Y)):
            Dist = 0.0
            for j in range(len(X)):
                Dist += (X[j] - Y[i, j]) ** 2
            Dist = np.sqrt(Dist)
            Soma += Dist
        return Soma / len(Y)

    # % Define the function to be optimized by nsga2
    def __ObjectiveGP(self, x):

        Fator = 1.0e10
        F = [None] * self.NObj
        xx = np.asarray(x).reshape(1, -1)

        Constraints = 0.0
        for cons in self.constraints:
            y = cons['fun'](x)
            if cons['type'] == 'eq':
                Constraints += np.abs(y)
            elif cons['type'] == 'ineq':
                if y < 0:
                    Constraints -= y

        for i in range(self.NObj):
            F[i] = -self.GP[i].predict(xx)[0] + Fator * Constraints

        return F

    # % __Sigmoid
    @staticmethod
    def __Sigmoid(x, k=10.):
        return 1. / (1. + np.exp(k * (x - 0.5)))


class MoboOpt(Algorithm):
    """ Hyperopt algorithms """

    def __init__(self, problem: Problem, name="Hyperopt"):
        super().__init__(problem, name)
        self.problem = problem

        self.options.declare(name='n_iterations', default=50, lower=1,
                             desc='Maximum evaluations')
        self.options.declare(name='n_init_samples', default=10, lower=1,
                             desc='Number of samples before optimization')

    def _objective(self, params):
        params_tmp = params.values()
        return self.evaluator.evaluate_scalar(params_tmp)

    def run(self):
        # Define the search space
        search_space = {}
        for parameter in self.problem.parameters:
            bounds = parameter['bounds']
            # search_space[parameter["name"]] = hp.uniform(parameter["name"], bounds[0], bounds[1])

        t_s = time.time()

        # self.problem.logger.info("Hyperopt: surr_name{}".format(self.options['surr_name']))
        self.problem.logger.info("Hyperopt: {}".format(""))

        best = 0

        t = time.time() - t_s
        self.problem.logger.info("Hyperopt: elapsed time: {} s".format(t))

        # sync changed individual informations
        self.problem.data_store.sync_all()

        if best is None:
            print('Optimization FAILED.')
            print('-' * 35)
        else:
            pass
            # print('Optimization Complete, %f seconds' % (clock() - start))
            # print("Result", x_out, mvalue)
            # print('-' * 35)
