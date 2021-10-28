from datetime import datetime


def get_dict_from_locals(locals_dict: dict, replace_underscore: bool = False, exclude: list = None):
    exclude = ('self', ) if exclude is None else tuple(['self'] + exclude)
    return {key if replace_underscore else key: value for key, value in
            locals_dict.items() if key not in exclude and '__py' not in key and value is not None}


def get_date_from_timestamp(date):
    return None if date is None else datetime.fromtimestamp(date)
