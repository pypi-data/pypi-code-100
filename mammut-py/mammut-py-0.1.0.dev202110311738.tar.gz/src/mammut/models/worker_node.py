# coding=utf-8

from mammut.models.node import Node

WORKER_NODE_JOB_NAME = "worker"


class WorkerNode(Node):
    def __init__(
        self,
        scope_name,
        configuration_path,
        configuration_name,
        task_index,
        redis_connection_pool=None,
    ):
        Node.__init__(
            self,
            scope_name,
            configuration_path,
            configuration_name,
            task_index,
            WORKER_NODE_JOB_NAME,
            redis_connection_pool,
        )
