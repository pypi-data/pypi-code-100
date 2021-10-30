import unittest

from ..results import Results
from ..benchmark_functions import Booth, AlpineFunction

from ..algorithm_mobopt import MOBayesian


class TestMOBayesianOptimization(unittest.TestCase):
    """ Tests simple one objective optimization problem."""

    def test_mobayesian_booth(self):
        problem = Booth()
        algorithm = MOBayesian(problem)
        algorithm.options['verbose_level'] = 1
        algorithm.options['n_iterations'] = 10
        algorithm.run()

        results = Results(problem)
        optimum = results.find_optimum(name='f_1')
        self.assertAlmostEqual(optimum.costs[0], 0, places=1)

    # def test_hyperopt_zdt1(self):
    #     problem = ZDT1(**{'dimension': 3})
    #     algorithm = Hyperopt(problem)
    #     # algorithm.options['verbose_level'] = 0
    #     algorithm.options['n_iterations'] = 200
    #     algorithm.run()
    #
    #     results = Results(problem)
    #     optimum = results.find_optimum(name='f_1')
    #     self.assertAlmostEqual(optimum.costs[0], problem.global_optimum, 1)
