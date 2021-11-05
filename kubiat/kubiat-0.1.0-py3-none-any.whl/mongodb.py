""" connection to mongodb """
import pymongo
from bson.objectid import ObjectId
import time
import os
from kubiat.service import APP
import constants

app_space = ''
if 'KUBIAT' in os.environ:
    app_space = os.environ['KUBIAT']
else:
    APP.logger.error('No App Space defined')
mongo_db_name = app_space

mongo_db_ip = 'kubiat-mongodb.mongodb'
if 'TEST' in os.environ:
    mongo_db_ip = 'localhost'

APP.logger.info('Running with IP: '+str(mongo_db_ip))
APP.logger.info('        with DB: '+constants._DB
                + ' ('+constants._ID+') on '+str(mongo_db_name))

myclient = pymongo.MongoClient('mongodb://root:admin@'+mongo_db_ip+':27017/')
mydb = myclient[mongo_db_name]


def convertTo_mid(key):
    mid_name = list(key.keys())[0]
    return {'_id': ObjectId(key[mid_name])}


def put_item_impl(table_name, key_name, item):
    item_copy = item.copy()
    item_copy['created_at'] = round(time.time())

    mycol = mydb[table_name]
    ret = mycol.insert_one(item_copy)
    item_copy[key_name] = str(item_copy.pop('_id'))
    return str(ret.inserted_id)


def put_items_impl(table_name, key_name, items):
    for item in items:
        item['created_at'] = round(time.time())

    mycol = mydb[table_name]
    ret = mycol.insert_many(items)
    for item in items:
        item[key_name] = str(item.pop('_id'))
    idlist = []
    for i in ret.inserted_ids:
        idlist.append(str(i))
    return idlist


def get_item_impl(table_name, key):
    item = mydb[table_name].find_one(convertTo_mid(key))
    if (item):
        item[list(key.keys())[0]] = str(item.pop('_id'))
    return item


def get_item_not_id_impl(table_name, key):
    item = mydb[table_name].find_one(key)
    if (item):
        item.pop('_id')
    return item


def get_items_impl(table_name, key_name, list_key_ids):
    items = []
    for orig_id in list_key_ids:
        item = get_item_impl(table_name, {key_name: orig_id})
        items.append(item)
    return items


# attr_dict is {attr_name_1:attr_value_1, ...}
def update_item_impl(table_name, key, attr_dict):
    attr_dict['last_updated'] = round(time.time())
    newvalues = {"$set": attr_dict}
    mydb[table_name].update_one(convertTo_mid(key), newvalues)
    return


def update_item_not_id_impl(table_name, key, attr_dict):
    attr_dict['last_updated'] = round(time.time())
    newvalues = {"$set": attr_dict}
    mydb[table_name].update_one(key, newvalues)
    return
