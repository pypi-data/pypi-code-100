import asyncio
from asyncio import Queue
from logging import Logger

from ..optimization import Evaluation
from .evaluation_planner import EvaluationPlanner
from .evaluator import Evaluator
from .supervisor import Supervisor


class Scheduler:
    """
    Plans and orchestrates the (potentially parallel) execution of evaluation processes.
    """

    def __init__(
        self,
        logger: Logger,
        max_parallel: int,
        evaluator: Evaluator,
        evaluation_planner: EvaluationPlanner,
        supervisor: Supervisor,
    ):
        self.__logger = logger
        self.__max_parallel = max_parallel
        self.__evaluator = evaluator
        self.__evaluation_planner = evaluation_planner
        self.__supervisor = supervisor

        self.__nr_of_running_evaluations = 0
        self.__evaluation_semaphore = None
        self.__scheduled_evaluations = None
        self.__errors = []

        self.__progress_needs_check = True

    async def run(self):
        self.__scheduled_evaluations = Queue()
        self.__evaluation_semaphore = asyncio.Semaphore(self.__max_parallel)

        tasks = []

        while True:
            self.__logger.debug(
                "Waiting for free evaluation slot.",
                extra={"currently_running": self.__nr_of_running_evaluations},
            )
            await self.__evaluation_semaphore.acquire()

            # before starting a possibly long running new async evaluation,
            # check progress and fill queue
            if self.__is_finished():
                break

            self.__fill_queue_if_empty()

            evaluation = self.__scheduled_evaluations.get_nowait()

            self.__nr_of_running_evaluations += 1
            task = asyncio.create_task(self.__evaluate(evaluation))
            tasks.append(task)

        await asyncio.gather(*tasks)

        self.__logger.debug("Evaluation processing loop finished.")

    def __is_finished(self):
        if len(self.__errors) > 0:
            self.__logger.error("One or more evaluations raised an error.")
            return True

        if self.__progress_needs_check:
            self.__progress_needs_check = False

            if self.__supervisor.is_process_finished():
                self.__logger.info("Stop criterion met.")
                return True

        return False

    def __fill_queue_if_empty(self):
        if self.__scheduled_evaluations.qsize() > 0:
            # no need to call API yet
            return

        # fill up to full parallel capacity without buffer
        desired = self.__max_parallel - self.__nr_of_running_evaluations

        new_evaluations = self.__evaluation_planner.generate(quantity=desired)

        for new_evaluation in new_evaluations:
            self.__scheduled_evaluations.put_nowait(new_evaluation)

    async def __evaluate(self, evaluation: Evaluation):
        try:
            await self.__evaluator.evaluate(evaluation)
        except Exception as e:
            self.__errors.append(e)
            raise e
        finally:
            self.__nr_of_running_evaluations -= 1
            self.__progress_needs_check = True
            self.__evaluation_semaphore.release()
