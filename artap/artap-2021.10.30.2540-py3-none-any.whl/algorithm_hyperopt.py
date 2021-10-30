from .problem import Problem
from .algorithm import Algorithm

import time

from hyperopt import fmin, tpe, hp


class Hyperopt(Algorithm):
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
            search_space[parameter["name"]] = hp.uniform(parameter["name"], bounds[0], bounds[1])

        t_s = time.time()

        # self.problem.logger.info("Hyperopt: surr_name{}".format(self.options['surr_name']))
        self.problem.logger.info("Hyperopt: {}".format(""))

        best = fmin(fn=self._objective,
                    space=search_space,
                    algo=tpe.suggest,
                    max_evals=self.options['n_iterations'])

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
