# -*- coding: utf-8 -*-
"""libjson module

"""
import json
from typing import Any, Union

from libumccr.utils import load_package_if_found


def dumps(data: Any, encoder=None) -> str:
    if encoder:
        return json.dumps(data, cls=encoder)

    elif load_package_if_found("django"):
        import django.core.serializers.json as django_ser
        return json.dumps(data, cls=django_ser.DjangoJSONEncoder)

    return json.dumps(data)


def loads(data: Union[str, bytes], decoder=None) -> Any:
    if decoder:
        return json.loads(data, cls=decoder)

    return json.loads(data)
