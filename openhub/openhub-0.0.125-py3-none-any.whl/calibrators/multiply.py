import logging
from raw_value_converter import RawValueConverter


class Sum(RawValueConverter):

    def perform_op(self, inputs):
        product = 1
        for input in inputs:
            product = product * input
        return product