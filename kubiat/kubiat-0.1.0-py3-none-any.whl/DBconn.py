from kubiat.mongodb import put_item_impl, put_items_impl
from kubiat.mongodb import get_item_impl, get_items_impl
from kubiat.mongodb import get_item_not_id_impl
from kubiat.mongodb import update_item_impl, update_item_not_id_impl
from constants import _DB, _ID


# returns id
def put_item(item):
    return put_item_impl(_DB, _ID, item)


# returns id list
def put_items(items):
    return put_items_impl(_DB, _ID, items)


def get_item(key):
    return get_item_impl(_DB, {_ID: key})


def get_items(list_key_ids):
    return get_items_impl(_DB, _ID, list_key_ids)


def get_item_not_id(key):
    return get_item_not_id_impl(_DB, {_ID: key})


# attr_dict is {attr_name_1:attr_value_1, ...}
def update_item(key, attr_dict):
    return update_item_impl(_DB, {_ID:  key}, attr_dict)


# attr_dict is {attr_name_1:attr_value_1, ...}
def update_item_not_id(key, attr_dict):
    return update_item_not_id_impl(_DB, {_ID: key}, attr_dict)
