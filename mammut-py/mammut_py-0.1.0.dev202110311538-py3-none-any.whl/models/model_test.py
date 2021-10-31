# coding=utf-8

import os.path
import tensorflow as tf
import numpy as np

from tensorflow.python.framework import test_util
from tensorflow.python.platform import googletest
from tensorflow.python.platform import tf_logging as logging

from mammut.models.parameter_node import ParameterNode
from mammut.models.worker_node import WorkerNode
from mammut.models.trainable_node import TrainableNode
from mammut.models.trainer import Trainer
from mammut.models import MODELS_CONFIGURATIONS_FILE_NAME


flags = tf.app.flags
FLAGS = flags.FLAGS


# flags.DEFINE_string('test_srcdir', '',
#                     'Dirctory with the source code.')
# flags.DEFINE_string(
#     "test_tmpdir", tf.test.get_temp_dir(), "Temporal Dirctory for data."
# )


class M_Node(ParameterNode):
    def __init__(self):
        ParameterNode.__init__(
            self, "parameter-m", "model-test", "parameter-m", 0, None
        )

    def _operation(self, *args, **kwargs):
        m = tf.Variable(tf.random_uniform([1], -1.0, 1.0), name="m")
        tf.summary.scalar("m", tf.gather(m, 0))
        return m


class MX_Node(WorkerNode):
    def __init__(self):
        WorkerNode.__init__(self, "worker-mx", "model-test", "worker-mx", 0, None)

    def _operation(self, *args, **kwargs):
        m_node = M_Node()
        x = args[0]
        return m_node() * x


class B_Node(ParameterNode):
    def __init__(self):
        ParameterNode.__init__(
            self, "parameter-b", "model-test", "parameter-b", 0, None
        )

    def _operation(self, *args, **kwargs):
        b = tf.Variable(tf.random_uniform([1], -1.0, 1.0), name="b")
        tf.summary.scalar("b", tf.gather(b, 0))

        return b


class LinearRegressorNode(TrainableNode):
    def __init__(self):
        TrainableNode.__init__(
            self, "linear-regresor", "model-test", "linear-regresor", 0, None
        )

    learning_rate = TrainableNode._add_configuration_property(
        "LinearRegressorNode",
        "learning_rate",
        0.5,
        float,
        "Indicates the learning rate of the gradient descent optimizer.",
    )

    def _operation(self, *args, **kwargs):
        x = args[0]
        mx_node = MX_Node()
        b_node = B_Node()

        return mx_node(x) + b_node()

    def _compute_loss(self, resultOp, expected_result):
        loss = tf.reduce_mean(tf.square(expected_result - resultOp))
        tf.summary.scalar("loss", loss)
        return loss

    def _optimize(self, global_step, loss_op):
        optimizer = tf.train.GradientDescentOptimizer(self.learning_rate)
        return [optimizer.minimize(loss_op, global_step), global_step]


class LinearRegressionTrainer(Trainer):
    def __init__(self):
        Trainer.__init__(self, "model-test", "linear-regresion-trainer", None)

    dataset_size = Trainer._add_configuration_property(
        "LinearRegressionTrainer",
        "dataset_size",
        2000,
        int,
        "Indicates the amounts of points to generate dataset.",
    )
    epoch_size = Trainer._add_configuration_property(
        "LinearRegressionTrainer",
        "epoch_size",
        200,
        int,
        "Indicates the amounts of points of the dataset used in each training epoch.",
    )
    step_size = Trainer._add_configuration_property(
        "LinearRegressionTrainer",
        "step_size",
        20,
        int,
        "Indicates the amounts of points of the dataset used in each training step.",
    )
    start_point = Trainer._add_configuration_property(
        "LinearRegressionTrainer",
        "start_point",
        10.1,
        float,
        "Indicates the start X point of the dataset.",
    )
    stop_point = Trainer._add_configuration_property(
        "LinearRegressionTrainer",
        "stop_point",
        200.1,
        float,
        "Indicates the end X point of the dataset.",
    )
    seed = Trainer._add_configuration_property(
        "LinearRegressionTrainer",
        "seed",
        1234,
        int,
        "Indicates the global seed to use.",
    )
    m = Trainer._add_configuration_property(
        "LinearRegressionTrainer",
        "m",
        60.5,
        float,
        "Indicates the slope used to compute Y point of the dataset.",
    )
    b = Trainer._add_configuration_property(
        "LinearRegressionTrainer",
        "b",
        30.2,
        float,
        "Indicates the Y axis intersection point used to compute Y point of the dataset.",
    )

    def _initialize_graph(self):
        self.current_dataset_point = 0
        self.current_epoch = 0
        # self.dataset_input_column = tf.linspace(self.start_point, self.stop_point, self.dataset_size, name="dataset_input_column")
        # self.dataset_input_column = np.linspace(self.start_point, self.stop_point, self.dataset_size, dtype=np.float32)
        # tf.set_random_seed(self.seed)
        np.random.seed(self.seed)
        # noise = tf.random_uniform([self.dataset_size], minval=0.0, maxval=0.5, name='noise')
        # noise = np.random.uniform(0.0, 0.5, self.dataset_size)
        # self.dataset_expected_result_column = ((self.m * self.dataset_input_column) + self.b) + noise
        # self.dataset_input_column = tf.random_uniform([self.dataset_size], self.start_point, self.stop_point, name="dataset_input_column")
        self.dataset_input_column = np.random.rand(self.dataset_size).astype(np.float32)
        self.dataset_expected_result_column = (
            self.dataset_input_column * self.m + self.b
        )

    def _recover_variables(self, sess):
        # self.dataset_input_column, self.dataset_expected_result_column = sess.run([self.dataset_input_column, self.dataset_expected_result_column])
        self.current_dataset_point = 0
        self.current_epoch = 0

    def _build_model(self) -> TrainableNode:
        return LinearRegressorNode()

    def _get_input_placeholder(self):
        return tf.placeholder(tf.float32, shape=(self.step_size), name="X")

    def _get_expectedResult_placeholder(self):
        return tf.placeholder(tf.float32, shape=(self.step_size), name="Y")

    def _fill_feed_dict(self, sess, input_placeholder, expected_result_placeholder):
        feed_dict = {
            input_placeholder: self.dataset_input_column[
                self.current_dataset_point : self.current_dataset_point + self.step_size
            ],
            expected_result_placeholder: self.dataset_expected_result_column[
                self.current_dataset_point : self.current_dataset_point + self.step_size
            ],
        }
        self.current_dataset_point = self.current_dataset_point + self.step_size
        if self.current_dataset_point % self.epoch_size == 0:
            self.current_epoch = self.current_epoch + 1
        return feed_dict

    def _get_current_epoch(self):
        return self.current_epoch


class ModelTest(test_util.TensorFlowTestCase):
    def setUp(self):
        # Creates a task context with the correct testing paths.
        MODELS_CONFIGURATIONS_FILE_NAME = os.path.join(FLAGS.test_tmpdir, "models.ini")

    def testLinearRegresor(self):
        """Test a simple linear regression model."""
        logging.info("Starting test...")
        trainer = LinearRegressionTrainer()
        final_loss = trainer.train(
            "tensorboard",
            int(trainer.dataset_size / trainer.epoch_size),
            log_step_mod=10,
        )
        logging.info("Final loss = {:-f}".format(final_loss))
        self.assertLessEqual(final_loss, 1.0, "Final loss greather than 1.")


if __name__ == "__main__":
    googletest.main()
