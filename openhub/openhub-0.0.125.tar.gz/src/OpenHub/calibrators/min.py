import logging
from raw_value_converter import RawValueConverter


class Min(RawValueConverter):

    def perform_op(self, inputs):
        return min(inputs)