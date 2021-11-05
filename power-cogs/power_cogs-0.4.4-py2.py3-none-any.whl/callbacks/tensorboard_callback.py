import os
from datetime import datetime

# internal
from power_cogs.callbacks.callback import Callback
from power_cogs.logging.tensorboard_logger import TensorboardLogger
from power_cogs.utils.utils import makedirs


class TensorboardCallback(Callback):
    def __init__(self, tensorboard_logger: TensorboardLogger = None, logging_config={}):
        super(TensorboardCallback, self).__init__()
        self.tensorboard_logger = tensorboard_logger
        self.logging_config = logging_config

    def _get_logging_path(self, checkpoint_path, logging_path, name: str):
        if logging_path is None:
            logging_path = makedirs(
                "{}_{}/".format(datetime.now().strftime("%Y-%m-%d-%H:%M:%S"), name)
            )
        return logging_path

    def setup(self, wrapped_class, f, *args, **kwargs):
        config = getattr(wrapped_class, "config", {})
        self.logging_config = config.get("logging_config", self.logging_config)

        checkpoint_path = self.logging_config.get("checkpoint_path", "checkpoints")
        name = self.logging_config.get("name", wrapped_class.__class__.__name__)

        logging_path = getattr(wrapped_class, "logging_path", None)
        logging_path = self._get_logging_path(checkpoint_path, logging_path, name)

        self.tensorboard_log_path = self.logging_config["tensorboard_log_path"]
        if self.tensorboard_log_path is None:
            self.tensorboard_log_path = makedirs(
                os.path.join(logging_path, "tensorboard_logs")
            )
        self.tensorboard_logger = TensorboardLogger(self.tensorboard_log_path)
        wrapped_class.tensorboard_logger = self.tensorboard_logger

    def after(self, prev_output, wrapped_class, f, *args, **kwargs):
        if self.tensorboard_logger is None:
            self.tensorboard_logger = getattr(wrapped_class, "tensorboard_logger")
        metrics = prev_output["metrics"]
        for metric in metrics:
            self.tensorboard_logger.log_scalar(
                metrics[metric], metric, step=metrics["epoch"]
            )
