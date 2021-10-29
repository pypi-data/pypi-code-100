import logging
from raw_value_converter import RawValueConverter


class Sum(RawValueConverter):

    def perform_op(self, inputs):
        if len(inputs) == 2:
            return inputs[0] - inputs[1]
        else:
            return 0