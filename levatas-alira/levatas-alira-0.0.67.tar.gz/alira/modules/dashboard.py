import logging

from alira.instance import Instance
from alira.modules import selection, flagging, module


PIPELINE_MODULE_NAME = "alira.modules.dashboard"


class Dashboard(module.Module):
    def __init__(self, image: str = None, attributes: dict() = None, **kwargs):
        super().__init__(PIPELINE_MODULE_NAME)

        self.attributes = attributes
        self.image = image

    def run(self, instance: Instance, **kwargs):
        result = {
            "prediction": "Positive" if instance.prediction == 1 else "Negative",
            "confidence": f"{(instance.confidence * 100):.2f}%",
        }

        if self.image:
            result["image"] = instance.get_attribute(self.image, default=instance.image)

        selected = False
        if selection.PIPELINE_MODULE_NAME in instance.properties:
            selected = (
                instance.properties[selection.PIPELINE_MODULE_NAME].get("selected", 0)
                == 1
            )

        flagged = False
        if flagging.PIPELINE_MODULE_NAME in instance.properties:
            flagged = (
                instance.properties[flagging.PIPELINE_MODULE_NAME].get("flagged", 0)
                == 1
            )

        result["selected"] = "Yes" if selected or flagged else "No"
        result["flagged"] = "Yes" if flagged else "No"

        if self.attributes:
            for attribute_name, attribute_label in self.attributes.items():
                try:
                    attribute_value = instance.get_attribute(attribute_name)
                    if "attributes" not in result:
                        result["attributes"] = dict()

                    result["attributes"][attribute_name] = {
                        "label": attribute_label,
                        "value": attribute_value,
                    }
                except AttributeError:
                    # If the attribute doesn't exist, we don't want to add it
                    # to the result.
                    pass

        return result
