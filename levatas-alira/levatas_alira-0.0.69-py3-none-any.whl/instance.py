import json


class Instance(object):
    def __init__(
        self,
        prediction: int = 1,
        confidence: float = 1.0,
        image: str = None,
        metadata: dict = None,
    ) -> None:
        self.prediction = prediction
        self.confidence = confidence
        self.image = image

        if metadata is not None and not isinstance(metadata, dict):
            raise ValueError("The field 'metadata' must be a dictionary.")

        self.metadata = metadata or {}
        self.properties = {}

    def has_attribute(self, name: str):
        try:
            self.get_attribute(name)
            return True
        except AttributeError:
            return False

    def get_attribute(self, name: str, *arg, **kwargs):
        def raise_exception(name: str, value):
            raise AttributeError(f"The attribute '{name}' does not exist.")

        def default_value(name, value):
            return value

        def get_attribute_from_dictionary(name: str, dictionary: dict):
            sections = name.split(".")

            if len(sections) == 1:
                try:
                    return dictionary[name]
                except KeyError:
                    raise AttributeError()

            index = 1

            while index < len(sections):
                name = ".".join(sections[:-index])

                if name in dictionary:
                    attribute = ".".join(sections[-index:])
                    return get_attribute_from_dictionary(attribute, dictionary[name])

                index += 1

            raise AttributeError()

        value = None
        attribute_doesnt_exist = raise_exception
        if "default" in kwargs:
            attribute_doesnt_exist = default_value
            value = kwargs["default"]

        elif len(arg) == 1:
            attribute_doesnt_exist = default_value
            value = arg[0]

        if name == "prediction":
            return self.prediction

        if name == "confidence":
            return self.confidence

        if name == "image":
            return self.image

        if name.startswith("metadata."):
            try:
                return get_attribute_from_dictionary(
                    name[len("metadata.") :], self.metadata
                )
            except AttributeError:
                return attribute_doesnt_exist(name, value)

        if name.startswith("properties."):
            try:
                return get_attribute_from_dictionary(
                    name[len("properties.") :], self.properties
                )
            except AttributeError:
                return attribute_doesnt_exist(name, value)

        return attribute_doesnt_exist(name, value)

    @staticmethod
    def create(data):
        data = data.copy()

        prediction = data.get("prediction", 1)
        confidence = data.get("confidence", 1.0)
        image = data.get("image", None)

        if "prediction" in data:
            del data["prediction"]

        if "confidence" in data:
            del data["confidence"]

        if "image" in data:
            del data["image"]

        metadata = Instance._format(data)

        instance = Instance(
            prediction=prediction, confidence=confidence, image=image, metadata=metadata
        )

        return instance

    @staticmethod
    def _format(data: dict) -> dict:
        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = Instance._format(value)
                continue

            # ML Metadata exclusively supports int, float, and str values. Anything else
            # we need to convert to a string.
            if not (
                isinstance(value, int)
                or isinstance(value, float)
                or isinstance(value, str)
            ):
                data[key] = json.dumps(value)

        return data


def onlyPositiveInstances(instance: Instance):
    return instance.prediction == 1


def onlyNegativeInstances(instance: Instance):
    return instance.prediction == 0
