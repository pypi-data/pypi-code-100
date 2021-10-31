# coding=utf-8

import tensorflow as tf
from abc import *
from mammut.models import DISTRIBUTED_TRAINING
from mammut.models.configurable import Configurable


class Node(Configurable):
    def __init__(
        self,
        scope_name,
        configuration_path,
        configuration_name,
        task_index,
        job_name,
        redis_connection_pool=None,
    ):
        Configurable.__init__(
            self, configuration_path, configuration_name, redis_connection_pool
        )
        self._scope = scope_name
        self._job = job_name
        self._task = task_index

    @abstractmethod
    def _operation(self, *args, **kwargs):
        ...

    def __call__(self, *args, **kwargs):
        if DISTRIBUTED_TRAINING:
            with tf.device("/job:{}/task:{:d}".format(self._job, self._task)):
                with tf.name_scope(self._scope):
                    return self._operation(args, kwargs)
        else:
            with tf.name_scope(self._scope):
                return self._operation(args, kwargs)
