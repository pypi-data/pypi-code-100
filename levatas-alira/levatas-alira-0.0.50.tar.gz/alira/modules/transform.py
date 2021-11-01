from alira.instance import Instance

PIPELINE_MODULE_NAME = "alira.modules.transform"


class Transform(object):
    def __init__(
        self,
        transform_fn: callable = None,
        **kwargs,
    ):
        self._pipeline_module_name = PIPELINE_MODULE_NAME
        self.transform_fn = transform_fn

        if self.transform_fn is not None and not callable(self.transform_fn):
            raise ValueError("The transformation function must be callable")

    def run(self, instance: Instance, **kwargs):
        if self.transform_fn:
            result = self.transform_fn(instance=instance, **kwargs)

            if not isinstance(result, dict):
                raise RuntimeError(
                    "The result of the transformation operation must be a dictionary"
                )

            return result

        return None
