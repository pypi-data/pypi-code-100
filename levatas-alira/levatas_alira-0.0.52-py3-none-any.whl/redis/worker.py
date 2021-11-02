import os
import logging
from time import sleep
from datetime import timedelta, datetime

import redis
from rq import Connection, Worker
from rq.job import Job
from rq_scheduler import Scheduler

START_INTERVAL = timedelta(seconds=4).total_seconds()
EXPONENTIAL_MAX_INTERVAL = timedelta(seconds=256).total_seconds()


def reenqueueing_failed_job(job_id):
    logging.info(f"Re-enqueueing failed job {job_id}")
    job = Job.fetch(job_id, connection=redis_connection)
    job.requeue()


def reenqueueing_failed_job_handler(job, exc_type, exception, traceback):
    if isinstance(exception, RuntimeError):
        # There are many reasons why a job can fail, but we only care about
        # those that are caused by a RuntimeError because they can be
        # rescheduled.

        job_id = job.get_id()
        job.refresh()

        delta = job.meta.get("delta_time", START_INTERVAL)
        delta = min(delta * 2, EXPONENTIAL_MAX_INTERVAL)

        job.meta["delta_time"] = delta
        job.save()

        logging.info(f"Re-enqueueing job {job_id} to run again in {delta} seconds")
        scheduler.enqueue_in(timedelta(seconds=delta), reenqueueing_failed_job, job_id)

        # Returning False prevents any other exception handlers to get executed.
        return False

    return True


def run_worker(redis_server: str, model_identifiers: list):
    logging.basicConfig(level=logging.INFO)

    global redis_connection
    redis_connection = redis.from_url(redis_server)

    global scheduler
    scheduler = Scheduler("failed", connection=redis_connection)

    with Connection(redis_connection):
        logging.info("Redis worker is running.")

        Worker(
            model_identifiers + ["failed"], exception_handlers=[reenqueueing_failed_job_handler]
        ).work()
