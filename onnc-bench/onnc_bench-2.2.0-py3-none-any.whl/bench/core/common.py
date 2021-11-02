import os
import tempfile


def get_class_name(model):
    c = model.__class__.__mro__[0]
    name = c.__module__ + "." + c.__name__
    return name


def get_tmp_path():
    return os.path.join(tempfile._get_default_tempdir(),
                        next(tempfile._get_candidate_names()))


def remove_if_exist(path):
    if type(path) != str:
        return
    if os.path.exists(path):
        os.remove(path)
