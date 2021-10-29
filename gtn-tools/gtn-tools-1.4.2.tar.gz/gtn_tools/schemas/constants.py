import enum


class Status(enum.Enum):
    NEW = "New"
    IN_PROGRESS = "In Progress"
    DONE = "Done"


class StatusPostEditing(enum.Enum):
    NEW = "New"
    IN_PROGRESS = "In Progress"
    POST_EDITING = "Post Editing"
    DONE = "Done"
