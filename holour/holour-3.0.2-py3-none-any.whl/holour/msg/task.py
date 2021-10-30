from typing import List
from holour.msg import Pose


class Task:

    STATUS_MISSING_PRECONDITION = "missing_precondition"
    STATUS_WAITING = "waiting"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_COMPLETED = "completed"
    STATUS_UNDO = "undo"
    STATUS_ERROR = "error"

    ASSIGNED_TO_HUMAN = "human"
    ASSIGNED_TO_ROBOT = "robot"

    def __init__(self, uuid: str, name: str, product_uuid: str, pose: Pose, automated: bool = False,
                 assigned_to: str = ASSIGNED_TO_HUMAN, conditions: List[str] = None, conditions_fulfilled: bool = True,
                 description: str = "", status: str = '', _type: str = ''):
        conditions = conditions if conditions else []
        status = status if status else self.STATUS_MISSING_PRECONDITION if len(conditions) > 0 else self.STATUS_WAITING
        assert type(uuid) == str
        assert type(name) == str
        assert type(product_uuid) == str
        assert type(pose) == Pose
        assert type(automated) == bool
        assert type(assigned_to) == str
        assert type(conditions) == list, f"Expected list type. Type of conditions: {type(conditions)}"
        assert type(conditions_fulfilled) == bool
        assert type(description) == str
        assert type(status) == str

        self._type = 'task'
        self.uuid = uuid
        self.name = name
        self.product_uuid = product_uuid
        self.pose = pose
        self.automated = automated
        self.assigned_to = assigned_to
        self.conditions = conditions
        self.conditions_fulfilled = conditions_fulfilled
        self.description = description
        self.status = status

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Task):
            return other.uuid == self.uuid \
                   and other.product_uuid == self.product_uuid \
                   and other.pose == self.pose \
                   and other.automated == self.automated \
                   and other.assigned_to == self.assigned_to \
                   and other.conditions == self.conditions \
                   and other.conditions_fulfilled == self.conditions_fulfilled \
                   and other.description == self.description \
                   and other.status == self.status
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __repr__(self):
        return f"<uuid={self.uuid},name={self.name},product_uuid={self.product_uuid},pose={self.pose}," \
               f"automated={self.automated},assigned_to={self.assigned_to},conditions={self.conditions}," \
               f"status={self.status},conditions_fulfilled={self.conditions_fulfilled},description={self.description}>"


class TaskMessage:

    def __init__(self, task_uuid: str, message: str, _type: str = ''):
        self._type = 'task_message'
        self.task_uuid = task_uuid
        self.message = message

    def __eq__(self, other: object) -> bool:
        if isinstance(other, TaskMessage):
            return other.task_uuid == self.task_uuid and other.message == self.message
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __repr__(self):
        return f"<task_uuid={self.task_uuid},message={self.message}>"
