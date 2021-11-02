from typing import List, TypedDict

from cff.models.record import Record


class LambdaEvent(TypedDict):
    """An event that triggers a Lambda invocation."""

    Records: List[Record]
    """Records of the events that raised *this* event."""
