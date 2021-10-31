from abc import abstractmethod, ABC
from mammut.curriculum.report.messages.message import CurriculumBaseMessage
import logging

log = logging.getLogger(__name__)


class BaseReporter(ABC):
    """Generic interface for Report components.

    A Reporter will report system messages that are important
    to users. These Messages uses the level threshold
    provided in python 'logging' package.

    Reporters use the same threshold level than python logging package.
    """

    def __init__(self, threshold=logging.INFO):
        """
        Args:
            threshold: threshold for this reporter.
        """
        self.threshold = threshold

    @abstractmethod
    def send_message(self, message: CurriculumBaseMessage, **kwargs):
        """
        Args:
            message: message to be reported.
            kwargs: any other required concrete parameter.
        """
        pass
