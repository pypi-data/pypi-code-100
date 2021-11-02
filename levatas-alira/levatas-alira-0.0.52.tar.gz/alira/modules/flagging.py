from time import time

from alira.instance import Instance
from alira.modules import module

PIPELINE_MODULE_NAME = "alira.modules.flagging"


class Flagging(module.Module):
    """Represents the default implementation for the flagging module. This module
    optimizes the decision of routing instances to a human using cost
    sensitivity criteria to reduce the cost of mistakes.

    Instances can overwrite the false positive, false negative, and human
    review costs used by this module by specifying a value for the `fp_cost`,
    `fn_cost`, and `human_review_cost` attributes::

        instance.metadata['fp_cost'] = 100
        instance.metadata['fn_cost'] = 300
        instance.metadata['human_review_cost'] = 10

    The costs specified as part of the instance will always be used over
    the costs specified for this module.

    Args:
        fp_cost(float): The cost of a false positive prediction. This argument
            is optional and when not specified, the module will
            simply mark as not flagged this instance.
        fn_cost(float): The cost of a false negative prediction. This argument
            is optional and when not specified, the module will
            simply mark as not flagged this instance.
        human_review_cost(float): The cost of a human review. This argument is
            optional and when not specified, the module will
            simply mark as not flagged this instance.
    """

    def __init__(
        self,
        fp_cost: float = None,
        fn_cost: float = None,
        human_review_cost: float = None,
        **kwargs,
    ):
        super().__init__(PIPELINE_MODULE_NAME)

        self.fp_cost = fp_cost or 0
        self.fn_cost = fn_cost or 0
        self.human_review_cost = human_review_cost or 0

    def run(self, instance: Instance, **kwargs):
        """Processes the supplied instance and returns a module result
        with a field indicates when the instance should be sent to a
        human review, and an element being a dictionary containing information
        about the computed costs.

        Here is an example of the result of this module::

            {
                "flagged": True,
                "cost_prediction_positive": 100,
                "cost_prediction_negative": 10,
            }

        Args:
            instance(dict): The instance that should be processed.
        Returns:
            dict: The instance result with the 'flagging' field
            settled with the flagging information.
        """

        # If the instance comes with specific costs, we want to use those
        # instead of the costs specified on this module.
        metadata = instance.metadata
        fp_cost = metadata.get("fp_cost", self.fp_cost)
        fn_cost = metadata.get("fn_cost", self.fn_cost)
        human_review_cost = metadata.get("human_review_cost", self.human_review_cost)
        prediction = instance.prediction
        confidence = instance.confidence

        cost_prediction_positive = (1 - confidence) * fp_cost
        cost_prediction_negative = confidence * fn_cost

        # Let's compute the likelihood of being wrong times
        # the cost of making a mistake.
        # If that cost is higher than the cost of asking for help, let's ask
        # for a human review.
        if (prediction == 1 and cost_prediction_positive > human_review_cost) or (
            prediction == 0 and cost_prediction_negative > human_review_cost
        ):
            return {
                "flagged": 1,
                "cost_prediction_positive": cost_prediction_positive,
                "cost_prediction_negative": cost_prediction_negative,
            }

        # At this point there's no upside to ask for a human review,
        # so let's continue without asking for help.
        return {
            "flagged": 0,
            "cost_prediction_positive": cost_prediction_positive,
            "cost_prediction_negative": cost_prediction_negative,
        }


class ConfidenceFlagging(module.Module):
    def __init__(self, min_confidence: float = 0.65, **kwargs):
        super().__init__(PIPELINE_MODULE_NAME)
        self.min_confidence = min_confidence

    def run(self, instance: dict, **kwargs):
        confidence = instance.confidence
        return {"flagged": int(confidence < self.min_confidence)}
