# coding=utf-8

from mammut.models.node import Node

PARAMETER_NODE_JOB_NAME = "ps"


class ParameterNode(Node):
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
            PARAMETER_NODE_JOB_NAME,
            redis_connection_pool,
        )
