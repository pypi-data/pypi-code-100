"""
Module for common application functionality for Lambda functions
"""
import sys
from abc import abstractmethod
from aws_lambda_powertools.utilities.data_classes.common import DictWrapper


class LambdaApplication:
    """
    Base class for Lambda applications
    """

    # Base class will always return event in same format
    EVENT_TYPE = DictWrapper

    def __init__(self, additional_log_config=None, load_ssm_params=False):
        self.context = None
        self.event = None
        self.sync_timer = None

    def main(self, event, context):
        """
        Common entry point behaviour
        """
        self.response = {"message": "Lambda application stopped"}
        try:
            self.context = context
            self.event = self.process_event(event)
            self.start()
            
        except InitialisationError as e:
            if self.log_object is None:
                print(e)
            else:
                self.log_object.write_log("LAMBDAINIT001", None, {"message": e})
            raise e
        except Exception as e:  # pylint:disable=broad-except
            if self.log_object is None:
                print(e)
            else:
                self.log_object.write_log(
                    "LAMBDA9999", sys.exc_info(), {"error": str(e)}
                )
            raise e

        return self.response

    @abstractmethod
    def start(self):
        """
        Start the application
        """

    def process_event(self, event):
        """
        Processes event object passed in by Lambda service
        Can be overridden to customise event parsing
        """
        return self.EVENT_TYPE(event)

    def initialise(self):
        """
        Application initialisation
        """


def overrides(base_class):
    """
    Decorator used to specify that a method overrides a base class method
    """

    def decorate(method):
        """
        Override assertion
        """
        assert method.__name__ in dir(base_class)
        return method

    return decorate


class InitialisationError(Exception):
    """
    Application initialisation error
    """

    def __init__(self, msg=None):
        super().__init__()
        self.msg = msg