import logging
from raw_value_converter import RawValueConverter


class Sum(RawValueConverter):

    def perform_op(self, inputs):
        return sum(inputs)