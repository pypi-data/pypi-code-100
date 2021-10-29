import logging
from abc import ABC, abstractmethod
import json


class RawValueConverter(ABC):
    logger = logging.getLogger(__name__)

    calibration_directory = None
    homekit_accessory_serial_no = None

    def __init__(self, channels=None, raw_value_converters=None):
        self.channels = channels
        self.raw_value_converters = raw_value_converters
        super().__init__()

    def run(self):
        outputs = []
        if self.raw_value_converters is not None:
            for converter in self.raw_value_converters:
                outputs.append(converter.run())
        if self.channels is not None:
            for channel in self.channels:
                outputs.append(channel.get_raw_value())

        return self.perform_op(outputs)

    @abstractmethod
    def perform_op(self, inputs):
        pass
