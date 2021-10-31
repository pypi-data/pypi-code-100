import logging

from alira.instance import Instance
from alira.modules import selection, flagging, module


PIPELINE_MODULE_NAME = "alira.modules.dashboard"


class Dashboard(module.Module):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(PIPELINE_MODULE_NAME)

    def run(self, instance: Instance, **kwargs):
        result = {
            "prediction": "Positive" if instance.prediction == 1 else "Negative",
            "confidence": f"{(instance.confidence * 100):.2f}%",
        }

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

        return result
