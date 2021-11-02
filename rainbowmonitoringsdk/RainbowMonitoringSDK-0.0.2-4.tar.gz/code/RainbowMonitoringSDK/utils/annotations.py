import json
import logging
import os
import subprocess
from functools import wraps
from time import time

from RainbowMonitoringSDK.probes.Metric import SimpleMetric, Metric
DOCKER_ID_LENGTH = 64

def get_entity_id():
    res = subprocess.Popen("head -1 /proc/self/cgroup|cut -d/ -f3", shell=True, stdout=subprocess.PIPE)
    encoded_first_line = res.stdout.readlines()[0].decode().replace("\n","")
    if len(encoded_first_line) != DOCKER_ID_LENGTH:
        logging.warning("This node probably is not containerised because has not container id")
        return None
    return encoded_first_line[:12]

class RainbowUtils:
    __ENTITY_ID__ = get_entity_id()
    __STORAGE_FILE__ = os.getenv("RAINBOW_METRIC_PATH", "./")+"rainbow.metrics.jsonl"
    __COUNT_IT_FUNCTIONS__ = {}

    @classmethod
    def store(cls, value, name, units, desc,
              minVal=float('-inf'), maxVal=float('inf'), higherIsBetter=True):
        simple_metric = SimpleMetric(name, units, desc, minVal, maxVal, higherIsBetter=higherIsBetter)
        simple_metric.set_val(value)
        cls.__store(simple_metric)

    @classmethod
    def __store(cls, metric: Metric):
        with open(cls.__STORAGE_FILE__, mode='a', encoding='utf-8') as file:
            new_name = cls.__container_enconded_name(metric)
            metric.set_name(new_name)
            metric_dict = metric.to_dict()
            json_metric = json.dumps(metric_dict) + '\n'
            file.write(json_metric)

    @classmethod
    def __container_enconded_name(cls, metric):
        if metric.name.startswith('_CGROUP_'):
            return metric.name
        prefix = '_CGROUP_' + cls.__ENTITY_ID__ + '__' if cls.__ENTITY_ID__ else ''
        new_name = prefix + metric.name  # Special name for
        return new_name

    @classmethod
    def timeit(cls, f):
        @wraps(f)
        def wrap(*args, **kw):
            ts = time()
            result = f(*args, **kw)
            te = time()
            name, unit, desc = "time__%s" % (f.__name__), 'ms', 'Execution duration from %s function' % (f.__name__)
            simple_metric = SimpleMetric(name, unit, desc, minVal=0.0, higherIsBetter=False)
            simple_metric.set_val(te - ts)
            cls.__store(simple_metric)
            return result

        return wrap

    @classmethod
    def export(cls, name, units, desc, minVal=float('-inf'), maxVal=float('inf'), higherIsBetter=True):
        def _export(f):
            simple_metric = SimpleMetric(name, units, desc, minVal=minVal, maxVal=maxVal, higherIsBetter=higherIsBetter)
            if not callable(f):
                simple_metric.set_val(f)
                cls.__store(simple_metric)
                return f

            @wraps(f)
            def wrap(*args, **kw):
                result = f(*args, **kw)
                if result is not None:
                    simple_metric.set_val(result)
                    cls.__store(simple_metric)
                else:
                    warning="Function %s returned None as result, monitoring can not capture this value" % f.__name__
                    logging.warning(warning)
                return result

            return wrap

        return _export

    @classmethod
    def countit(cls, f):
        @wraps(f)
        def wrap(*args, **kw):
            result = f(*args, **kw)
            functions, function_name = cls.__COUNT_IT_FUNCTIONS__, f.__name__
            if function_name not in functions:
                functions[function_name] = 0
            functions[function_name] += 1
            name, unit, desc = "countit__%s" % function_name, 'runs', 'The running times of %s function' % function_name
            simple_metric = SimpleMetric(name, unit, desc, minVal=0.0, higherIsBetter=False)
            simple_metric.set_val(functions[function_name])
            cls.__store(simple_metric)
            return result

        return wrap
