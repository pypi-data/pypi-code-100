import qecstruct as qs
import multiprocess as mup

import math
from pandas import DataFrame

class Laboratory:
    def __init__(self, rng_seed=None, num_processes=1):
        self.rng = qs.Rng(rng_seed)
        self.num_processes = num_processes
        self.experiments = list()
        self.extras = list()

    def add_experiment(self, experiment, extras=None):
        self.experiments.append(experiment)
        self.extras.append(extras)

    def run_all_while(self, condition):
        def runner(experiment, rng):
            return experiment.run_while(condition, rng)
        return self._run(runner)

    def _run(self, runner):
        rngs = [self.rng.jump() for _ in range(len(self.experiments))]
        with mup.Pool(self.num_processes) as pool:
            statistics = pool.map(runner, zip(self.experiments, rngs))
        data = DataFrame()
        for (experiment, stats, extras) in zip(self.experiments, statistics, self.extras):
            data.append(
                convert_to_dataframe(experiment, stats, extras),
                sort=True
            )
        return data

class Statistics:
    def __init__(self):
        self.num_successes = 0
        self.num_failures = 0

    @property
    def num_samples(self):
        return self.num_successes + self.num_failures
    
    def add_success(self):
        self.num_successes += 1
            
    def add_failures(self):
        self.num_failures += 1

    def success_rate(self):
        return self.num_successes / self.num_samples

    def failure_rate(self):
        return self.num_failures / self.num_samples

    def variance(self):
        return self.failure_rate() * self.success_rate() / self.num_samples
        
    def std(self):
        return math.sqrt(self.variance())

    def __repr__(self):
        string = "Statistics\n"
        string += "----------\n"
        string += f"number of samples: {self.num_samples}\n"
        if self.sample_size() > 0:
            string += f"failure rate: {self.failure_rate()}\n"
            string += f"success rate: {self.success_rate()}\n"
            string += f"standard deviation: {self.std()}"
        return string


class LinearDecodingExperiment:
    def __init__(self, code, decoder, noise):
        self.code = code
        self.decoder = decoder
        self.noise = noise

    def run_once(self, rng):
        codeword = self.code.random_codeword(rng)
        error = self.noise.sample(len(self.code), rng)
        guess = self.decoder.decode(codeword + error)
        if guess is not None:
            return codeword == guess  
        else:
            return False

    def run_while(self, condition, rng):
        statistics = Statistics()
        while condition(statistics):
            if self.run_once(rng):
                statistics.add_success()
            else:
                statistics.add_failures()
        return statistics

    def run_until(self, condition, rng):
        while_condition = lambda stat: not condition(stat)
        return self.run_while(while_condition, rng)

    def run_num_times(self, num_samples, rng):
        condition = lambda stat: stat.num_samples < num_samples
        return self.run_while(condition, rng)


def convert_to_dataframe(experiment, statistics, extras=dict()):
    data = {
        "Block length": len(experiment.code),
        "Dimension": experiment.code.dimension(),
        "Physical error rate": experiment.noise.error_probability(),
        "Number of experiments": statistics.num_experiments(),
        "Logical failure rate": statistics.failure_rate(),
        "Standard deviation": statistics.std(),
    }
    data.update(extras)
    return DataFrame(data)
