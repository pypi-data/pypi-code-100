from enum import Enum


class PontemOrderStatuses(str, Enum):
    REJECTED = "Rejected"
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    NOT_STARTED = "Not Started"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    FULFILLED = "Fulfilled"
    EXPIRED = "Expired"

    def __str__(self) -> str:
        return str(self.value)
