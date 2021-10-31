# coding=utf-8

from abc import *
from mammut.models.worker_node import WorkerNode

import tensorflow as tf


class TrainableNode(WorkerNode):
    def __init__(
        self,
        scope_name,
        configuration_path,
        configuration_name,
        task_index,
        redis_connection_pool=None,
    ):
        WorkerNode.__init__(
            self,
            scope_name,
            configuration_path,
            configuration_name,
            task_index,
            redis_connection_pool,
        )

    @abstractmethod
    def _compute_loss(self, resultOp, expected_result):
        ...

    @abstractmethod
    def _optimize(sel, global_step, loss_op):
        ...

    def training_step_op(self, global_step, input, expected_result):
        """"""

        # Evaluate the model. This returns the operation asociated to this node.
        result_op = self(input)
        loss_op = self._compute_loss(result_op, expected_result)
        optimize_op, global_step = self._optimize(global_step, loss_op)

        return [optimize_op, loss_op, global_step]
