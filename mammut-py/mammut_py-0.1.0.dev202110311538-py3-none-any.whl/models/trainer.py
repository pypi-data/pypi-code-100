# coding=utf-8

from abc import *
import tensorflow as tf
import time
import os.path

from tensorflow.python.platform import tf_logging as logging
from mammut.models.trainable_node import TrainableNode
from mammut.models import DISTRIBUTED_TRAINING
from mammut.models.parameter_node import PARAMETER_NODE_JOB_NAME
from mammut.models.configurable import Configurable


class Trainer(Configurable):
    def __init__(
        self, configuration_path, configuration_name, redis_connection_pool=None
    ):
        Configurable.__init__(
            self, configuration_path, configuration_name, redis_connection_pool
        )

    @abstractmethod
    def _initialize_graph(self):
        ...

    # TODO: Este metodo no se llamara hasta setear el init_fn del supervisor.
    @abstractmethod
    def _recover_variables(self, sess):
        ...

    @abstractmethod
    def _build_model(self) -> TrainableNode:
        ...

    @abstractmethod
    def _get_input_placeholder(self):
        ...

    @abstractmethod
    def _get_expectedResult_placeholder(self):
        ...

    @abstractmethod
    def _fill_feed_dict(self, sess, input_placeholder, expected_result_placeholder):
        ...

    @abstractmethod
    def _get_current_epoch(self):
        ...

    def train(
        self,
        logdir,
        max_epochs,
        ps_hosts=None,
        worker_hosts=None,
        job_name=None,
        task_index=None,
        save_summaries_secs=200,
        save_model_secs=300,
        log_step_mod=100,
    ):

        graph = tf.Graph()
        with graph.as_default():

            is_chief = True  ## Default value
            target = ""
            is_parameter_server = False

            if DISTRIBUTED_TRAINING:
                logging.info("Distributed training active")
                if ps_hosts != None:
                    # Create a cluster from the parameter server and worker hosts.
                    cluster = tf.train.ClusterSpec(
                        {"ps": ps_hosts, "worker": worker_hosts}
                    )
                    # Create and start a server for the local task.
                    server = tf.train.Server(
                        cluster, job_name=job_name, task_index=task_index
                    )
                    if job_name == PARAMETER_NODE_JOB_NAME:
                        is_parameter_server = True
                        server.join()
                    # Check if the supervisor must be mark as chief
                    is_chief = task_index == 0
                    target = server.target

            if not is_parameter_server:
                if DISTRIBUTED_TRAINING:
                    with tf.device(
                        "/job:{}/task:{:d}".format(PARAMETER_NODE_JOB_NAME, 0)
                    ):
                        # step counter used in summaries and checkpoint filenames.
                        global_step = tf.Variable(
                            0, trainable=False, name="global_step"
                        )
                else:
                    global_step = tf.Variable(0, trainable=False, name="global_step")

                # Build the model
                self._initialize_graph()
                trainable_node = self._build_model()

                # Get the training step
                input_placeholder = self._get_input_placeholder()
                expected_result_placeholder = self._get_expectedResult_placeholder()

                # operations
                training_step_op = trainable_node.training_step_op(
                    global_step, input_placeholder, expected_result_placeholder
                )

                # Build the summary Tensor based on the TF collection of Summaries.
                summary_op = tf.summary.merge_all()
                training_step_op = [summary_op] + training_step_op

                # Add ops to save and restore all the variables.
                # Saver only captures all variables at the time it is constructed, so any new variables defined
                # after Saver() will not be saved/restored automatically.
                saver = None
                summary_writer = None
                if logdir != None:
                    saver = tf.train.Saver()
                    summary_writer = tf.summary.FileWriter(logdir, graph)

                # TODO: This class tf.train.Supervisor is deprecated. Please use tf.train.MonitoredTrainingSession instead.
                # Create a "supervisor", which oversees the training process.
                sv = tf.train.Supervisor(
                    is_chief=is_chief,
                    logdir=logdir,
                    # init_op=None, # Init function to manually recover a model
                    summary_op=None,
                    saver=saver,
                    global_step=global_step,
                    save_summaries_secs=save_summaries_secs,
                    save_model_secs=save_model_secs,
                    summary_writer=summary_writer,
                    init_fn=self._recover_variables,
                )

                # TODO: Agregar parametro para configurar el uso de init_op/init_fn

                with sv.managed_session(
                    master=target,
                    config=tf.ConfigProto(
                        allow_soft_placement=True, log_device_placement=True
                    ),
                ) as sess:

                    while (
                        not sv.should_stop() and self._get_current_epoch() < max_epochs
                    ):
                        start_time = time.time()

                        # Feed in data for session run
                        feed_dict = self._fill_feed_dict(
                            sess, input_placeholder, expected_result_placeholder
                        )

                        # Run session
                        summary, _, loss_value, step = sess.run(
                            training_step_op, feed_dict=feed_dict
                        )

                        # Append summary
                        sv.summary_computed(sess, summary)

                        current_step = int(step)

                        if current_step % log_step_mod == 0:
                            duration = time.time() - start_time
                            logging.info(
                                "Step %d: loss = %.2f (%.3f sec)"
                                % (step, loss_value, duration)
                            )

                sv.stop()

                return float(loss_value)

            else:
                return -1.0

    # TODO: falta colocar la logica para automaticamente evaluar el modelo contra los datasets de validacion y pruebas cada cierta cantidad de epocas
