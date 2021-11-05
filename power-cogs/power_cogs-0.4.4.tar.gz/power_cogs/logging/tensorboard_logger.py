import os

from loguru import logger
from torch.utils.tensorboard import SummaryWriter

from power_cogs.logging.logger_utils import doublewrap, safe
from power_cogs.utils.utils import makedirs  # noqa


class TensorboardLogger:
    def __init__(
        self, tensorboard_log_path: str = "./tensorboard_logs", logging_path=None
    ):
        self.logging_path = logging_path
        if self.logging_path is not None:
            tensorboard_log_path = makedirs(
                os.path.join(logging_path, tensorboard_log_path)
            )
        self.tensorboard_run_path = os.path.abspath(
            os.path.join(tensorboard_log_path, "default")
        )
        self.tensorboard_writer = self.create_tensorboard(self.tensorboard_run_path)
        logger.info(
            "Follow tensorboard logs with: tensorboard --logdir {}".format(
                self.tensorboard_run_path
            )
        )

    def create_tensorboard(self, tensorboard_run_path: str):
        tensorboard_writer = SummaryWriter(tensorboard_run_path)
        return tensorboard_writer

    @safe
    def close(self):
        self.tensorboard_writer.close()


@doublewrap
def tensorboard(cls):
    class TensorboardWrapper(cls):
        def __init__(self, *args, **kwargs):
            self.logger = TensorboardLogger()
            self.__name__ = cls.__name__
            super().__init__(*args, **kwargs)

        def __repr__(self):
            return repr(cls)

        def log_scalar(self, *args, **kwargs):
            self.logger.log_scalar(*args, **kwargs)

        def log_text(self, *args, **kwargs):
            self.logger.log_text(*args, **kwargs)

        def close(self):
            self.logger.close()

    return TensorboardWrapper
