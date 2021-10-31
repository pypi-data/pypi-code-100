import random

from time import time

from ml_metadata.proto import metadata_store_pb2
from ml_metadata.errors import NotFoundError


class StaticSelection(object):
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
        self.name = "alira.StaticSelection"
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

        return {
            "selected": int(value < self.percentage)
        }

    def register(self, store):
        try:
            component_execution_type = store.get_execution_type(type_name=self.name + "Type")
            component_execution_type_id = component_execution_type.id
        except NotFoundError:
            component_execution_type = metadata_store_pb2.ExecutionType()
            component_execution_type.name = self.name + "Type"
            component_execution_type.properties["name"] = metadata_store_pb2.STRING
            component_execution_type.properties["percentage"] = metadata_store_pb2.DOUBLE
            component_execution_type_id = store.put_execution_type(component_execution_type)

        component_execution = metadata_store_pb2.Execution()
        component_execution.type_id = component_execution_type_id
        component_execution.last_known_state = metadata_store_pb2.Execution.State.NEW
        component_execution.properties["name"].string_value = self.name
        component_execution.properties["percentage"].double_value = self.percentage
        component_execution.create_time_since_epoch = int(time() * 1000)
        [component_execution_id] = store.put_executions([component_execution])
        component_execution.id = component_execution_id

        try:
            output_artifact_type = store.get_artifact_type(type_name=self.name + "Output")
        except NotFoundError:
            output_artifact_type = metadata_store_pb2.ArtifactType()
            output_artifact_type.name = self.name + "Output"
            output_artifact_type.properties["selected"] = metadata_store_pb2.INT
            output_artifact_type_id = store.put_artifact_type(output_artifact_type)
            output_artifact_type.id = output_artifact_type_id
        
        return component_execution, output_artifact_type