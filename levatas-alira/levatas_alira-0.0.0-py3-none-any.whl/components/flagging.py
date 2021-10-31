from time import time

from ml_metadata.proto import metadata_store_pb2
from ml_metadata.errors import NotFoundError

from ..instance import Instance


class Flagging(object):
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
        **kwargs
    ):
        self.fp_cost = fp_cost
        self.fn_cost = fn_cost
        self.human_review_cost = human_review_cost
        self.name = "alira.Flagging"

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
        human_review_cost = metadata.get(
            "human_review_cost", self.human_review_cost
        )
        classification = instance.classification
        confidence = instance.confidence

        cost_prediction_positive = (1 - confidence) * fp_cost
        cost_prediction_negative = confidence * fn_cost

        # Let's compute the likelihood of being wrong times
        # the cost of making a mistake.
        # If that cost is higher than the cost of asking for help, let's ask
        # for a human review.
        if (classification == 1 and cost_prediction_positive > human_review_cost) or (
            classification == 0 and cost_prediction_negative > human_review_cost
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

    def register(self, store):
        try:
            component_execution_type = store.get_execution_type(type_name=self.name + "Type")
            component_execution_type_id = component_execution_type.id
        except NotFoundError:
            component_execution_type = metadata_store_pb2.ExecutionType()
            component_execution_type.name = self.name + "Type"
            component_execution_type.properties["name"] = metadata_store_pb2.STRING
            component_execution_type.properties["fp_cost"] = metadata_store_pb2.DOUBLE
            component_execution_type.properties["fn_cost"] = metadata_store_pb2.DOUBLE
            component_execution_type.properties["human_review_cost"] = metadata_store_pb2.DOUBLE
            component_execution_type_id = store.put_execution_type(component_execution_type)

        component_execution = metadata_store_pb2.Execution()
        component_execution.type_id = component_execution_type_id
        component_execution.last_known_state = metadata_store_pb2.Execution.State.NEW
        component_execution.properties["name"].string_value = self.name
        component_execution.properties["fp_cost"].double_value = self.fp_cost
        component_execution.properties["fn_cost"].double_value = self.fn_cost
        component_execution.properties["human_review_cost"].double_value = self.human_review_cost
        component_execution.create_time_since_epoch = int(time() * 1000)
        [component_execution_id] = store.put_executions([component_execution])
        component_execution.id = component_execution_id

        try:
            output_artifact_type = store.get_artifact_type(type_name=self.name + "Output")
        except NotFoundError:
            output_artifact_type = metadata_store_pb2.ArtifactType()
            output_artifact_type.name = self.name + "Output"
            output_artifact_type.properties["flagged"] = metadata_store_pb2.INT
            output_artifact_type.properties["cost_prediction_positive"] = metadata_store_pb2.DOUBLE
            output_artifact_type.properties["cost_prediction_negative"] = metadata_store_pb2.DOUBLE
            output_artifact_type_id = store.put_artifact_type(output_artifact_type)
            output_artifact_type.id = output_artifact_type_id
        
        return component_execution, output_artifact_type

class ConfidenceFlagging(object):
    def __init__(
        self,
        min_confidence: float = 0.65,
        **kwargs
    ):
        self.name = "alira.ConfidenceFlagging"
        self.min_confidence = min_confidence

    def run(self, instance: dict, **kwargs):
        confidence = instance.confidence
        return {
            "flagged": int(confidence < self.min_confidence)
        }

    def register(self, store):
        try:
            component_execution_type = store.get_execution_type(type_name=self.name + "Type")
            component_execution_type_id = component_execution_type.id
        except NotFoundError:
            component_execution_type = metadata_store_pb2.ExecutionType()
            component_execution_type.name = self.name + "Type"
            component_execution_type.properties["name"] = metadata_store_pb2.STRING
            component_execution_type.properties["threshold"] = metadata_store_pb2.DOUBLE
            component_execution_type_id = store.put_execution_type(component_execution_type)

        component_execution = metadata_store_pb2.Execution()
        component_execution.type_id = component_execution_type_id
        component_execution.last_known_state = metadata_store_pb2.Execution.State.NEW
        component_execution.properties["name"].string_value = self.name
        component_execution.properties["threshold"].double_value = self.min_confidence
        component_execution.create_time_since_epoch = int(time() * 1000)
        [component_execution_id] = store.put_executions([component_execution])
        component_execution.id = component_execution_id

        try:
            output_artifact_type = store.get_artifact_type(type_name=self.name + "Output")
        except NotFoundError:
            output_artifact_type = metadata_store_pb2.ArtifactType()
            output_artifact_type.name = self.name + "Output"
            output_artifact_type.properties["flagged"] = metadata_store_pb2.INT
            output_artifact_type_id = store.put_artifact_type(output_artifact_type)
            output_artifact_type.id = output_artifact_type_id
        
        return component_execution, output_artifact_type
