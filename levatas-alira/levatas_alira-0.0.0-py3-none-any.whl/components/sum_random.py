import logging
import random

from .asynchronous import AsynchronousModule


logger = logging.getLogger(__name__)


def sum(value1, value2):
    logger.info("Result: {}.".format(value1 + value2))


class SumRandom(AsynchronousModule):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.name = "alira.SumRandom"

    def run(self, **kwargs):
        arguments = {
            "value1": random.random(),
            "value2": random.random()
        }
        queue = self._get_queue()
        if queue:
            job = queue.enqueue(sum, **arguments)
            result = {}

            if self.job_field:
                    result[self.job_field] = job.get_id()

            return result

        return {
            "sum": sum(**arguments)
        }
