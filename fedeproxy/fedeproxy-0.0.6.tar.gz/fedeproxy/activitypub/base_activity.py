from dataclasses import dataclass
from json import JSONEncoder


class ActivitySerializerError(ValueError):
    ...


class ActivityEncoder(JSONEncoder):
    def default(self, o):
        return o.to_dict()


@dataclass
class Signature:
    creator: str
    created: str
    signatureValue: str
    type: str = "RsaSignature2017"


def naive_parse(activity_objects, activity_json, serializer=None):
    """this navigates circular import issues"""
    if not serializer:
        if activity_json.get("publicKeyPem"):
            # ugh
            activity_json["type"] = "PublicKey"

        activity_type = activity_json.get("type")
        try:
            serializer = activity_objects[activity_type]
        except KeyError as err:
            # we know this exists and that we can't handle it
            if activity_type in ["Question"]:
                return None
            raise ActivitySerializerError(err)

    return serializer(activity_objects=activity_objects, **activity_json)


@dataclass
class ActivityObject:
    id: str = None
    type: str = None
