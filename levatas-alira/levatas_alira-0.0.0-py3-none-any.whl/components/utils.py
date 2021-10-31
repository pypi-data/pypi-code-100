from ..instance import Instance


ONLY_POSITIVE_INSTANCES = "onlyPositiveInstances"
ONLY_NEGATIVE_INSTANCES = "onlyNegativeInstances"
EVERY_INSTANCE = "everyInstance"


def has_to_notify(
    instance: Instance,
    notification,
    **kwargs
) -> bool:
    if callable(notification):
        return notification(
            instance=instance,
            **kwargs
        )

    if notification == ONLY_POSITIVE_INSTANCES:
        return bool(instance.classification)

    if notification == ONLY_NEGATIVE_INSTANCES:
        return not bool(instance.classification)

    return True


def add_pipeline_id(pipeline_id: int, **kwargs):
    return {
        "pipeline_id": pipeline_id
    }