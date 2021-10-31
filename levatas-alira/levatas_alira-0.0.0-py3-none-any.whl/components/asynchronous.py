import os
import redis

from rq import Queue


class AsynchronousModule(object):
    def __init__(
        self,
        job_scheduler_server: str = "redis://redis:6379/1",
        asynchronous: bool = True,
        job_field: str = "async_job",
        queue_name: str = None,
        **kwargs
    ):
        self.job_scheduler_server = job_scheduler_server
        self.asynchronous = asynchronous
        self.job_field = job_field

        model_base_directory =  kwargs.get(
            "model_base_directory",
            "/opt/ml/alira"
        )
        model_identifier = os.path.basename(model_base_directory)
        if queue_name is None:
            queue_name = model_identifier

        self.queue_name = queue_name

    def _get_queue(self):
        if self.job_scheduler_server is not None:
            redis_connection = redis.from_url(self.job_scheduler_server)
            return Queue(
                self.queue_name, connection=redis_connection, is_async=self.asynchronous
            )

        return None