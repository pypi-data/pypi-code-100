__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"

from .get_table_foreignkey_param import get_table_fields, get_table_foreignkey_param
import json

def set_table_default_value(obj_to_mod):
    """
    如果某些参数没设置，则设置默认值
    """
    i = obj_to_mod
    if i.table_name is None or i.table_name=='':
        return 'nothing to change'

    if i.inspected_from_db is None:
        i.inspected_from_db=1
    if (i.is_managed is None) or (i.is_managed==''):
        i.is_managed=1
    if (i.route is None) or (i.route ==''):
        i.route='/' + i.table_name.title()
    if (i.table_big_name is None) or (i.table_big_name==''):
        i.table_big_name = i.table_name.title()
    if i.foreign_key_id is None:
        i.foreign_key_id = get_table_foreignkey_param(i.table_name)
    if i.ordering_fields is None:
        field_list = get_table_fields(i.table_name)
        i.ordering_fields = field_list
    if i.ordering is None:
        field_list = get_table_fields(i.table_name)
        i.ordering =  field_list
    if i.search_fields is None:
        #搜索项不能有外键
        field_list = get_table_fields(i.table_name, 0)
        i.search_fields = field_list
    if i.no_need_login is None:
        i.no_need_login = 1

    if (i.foreign_key_ro is None) or (i.foreign_key_ro==''):
        foreign_key = get_table_foreignkey_param(i.table_name,1)
        i.foreign_key_ro={}
        for j in foreign_key:
            field_list = get_table_fields(foreign_key[j][2], 0)
            for k in field_list:
                i.foreign_key_ro[str(j)+'_' + str(k)] = str(j)+'.' + str(k)




    if i.model_object_list is None:
        field_list = get_table_fields(i.table_name)
        i.model_object_list = field_list



    i.save()
    return 'ok'