import random

from time import time
from alira.modules import module

PIPELINE_MODULE_NAME = "alira.modules.selection"


class Selection(module.Module):
    """
    Selects a percentage of instances as they go through the workflow and
    redirects them for human review.

    Having a group of instances reviewed by humans gives the workflow
    a baseline understanding of its performance, and allows it to compute
    metrics that can later be extrapolated to all processed instances
    by the workflow.

    To make sure the group of instances selected by this module is
    statistically valid, this implementation doesn't rely on any
    of the data attached to the instance to
    make a decision of whether it should be selected for review.

    Usage::

        from alira.components import StaticSelection

        selection = StaticSelection(percentage=0.1)

    Args:
        percentage(float): The percentage of instances that should be selected
            for human review. This attribute is optional, and if not specified,
            20% of the instances will be selected.

    Attributes:
        percentage(float): The percentage of instances that should be selected
            for human review. This attribute is optional, and if not specified,
            20% of the instances will be selected.

        name(string): The component's name

    Raises:
        ValueError: If `percentage` is either less than 0.0
        or greater than 1.0.
    """

    def __init__(self, percentage: float = 0.2, **kwargs):
        super().__init__(PIPELINE_MODULE_NAME)

        if percentage < 0.0 or percentage > 1.0:
            raise ValueError("The specified percentage should be between [0.0..1.0]")

        self.percentage = percentage

    def run(self, **kwargs):
        """
        Processes the supplied instances and set a boolean value indicating
        whether it should be selected for human review.

        Args:
            instance(dict): The instance that should be processed.
        Returns:
            int: The instance result equal to 1
            if the instance should be sent for human review. 0 otherwise.
        """
        value = random.random()

        return {"selected": int(value < self.percentage)}
