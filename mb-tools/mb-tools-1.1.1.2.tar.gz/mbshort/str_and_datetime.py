from datetime import datetime
from functools import partial


def datetime_filter(obj):
    if isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return obj


def datetime_filter_tz(obj):
    if isinstance(obj, datetime):
        return obj.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    else:
        return obj


def orm_to_dict_with_filter(obj, model, filter=datetime_filter):
    """ orm对象转成字典,接口里面少用, 因为接口应该是明确的稳定的, 不能随orm而变动 """
    return {c.name: filter(getattr(obj, c.name)) for c in model.__table__.columns}


orm_to_dict = partial(orm_to_dict_with_filter, filter=datetime_filter)
orm_to_dict_tz = partial(orm_to_dict_with_filter, filter=datetime_filter_tz)
