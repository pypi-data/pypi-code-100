import os
import redis

from rq import Queue

from alira.modules import module


class RedisModule(module.Module):
    def __init__(
        self, pipeline_module_name, model_identifier, model_directory, redis_server: str
    ):
        super().__init__(pipeline_module_name)

        self.model_directory = model_directory
        self.redis_server = redis_server
        self.queue_name = model_identifier

    def get_redis_queue(self):
        if self.redis_server:
            redis_connection = redis.from_url(self.job_scheduler_server)
            return Queue(self.queue_name, connection=redis_connection, is_async=True)

        return None
