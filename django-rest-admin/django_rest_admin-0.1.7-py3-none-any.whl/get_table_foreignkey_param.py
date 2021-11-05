__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"
import re

def get_models_param_from_inspectdb(table_name, add_real_table_name=0):
    """
        {"user":["User", "CASCADE"], "article":["Article", "SET_NULL"]}'
    """
    from django.core.management import call_command
    import os

    if table_name is None or table_name == '':
        return {}

    foreign_key_id = {}

    # 保存inspectdb数据到stringio.
    f = io.StringIO()
    call_command("inspectdb", [table_name], stdout=f)
    # 所有数据读出到字符串变量：models_new
    models_new = f.getvalue()
    f.close()

    # 解析每一行，获取外键信息
    for one_line in models_new.split('\n'):
        # 每行分析处理
        if len(one_line.strip()) == 0:
            # 空行
            continue
        one_line_start_space = len(one_line) - len(one_line.lstrip())
        one_line_striped = one_line.strip()
        if one_line_striped[0] == '#':
            # 注释
            continue

        spt = one_line_striped.split(' ')
        if len(spt) == 0:
            # 没有空格，不认识的行??
            continue

        if (one_line_start_space == 0) and (spt[0] == 'class'):
            # 获取类名
            curr_class_name = spt[1].split('(')[0]
            continue

        curr_field_name = spt[0]
        if curr_field_name == 'id':
            # id自动去除，避免djanog错误
            continue

        if len(spt) > 2 and 'models.ForeignKey(' in spt[2]:
            foreign_table_name = spt[2].split('\'')[1]
            foreign_on_delete = spt[3]
            foreign_on_delete = foreign_on_delete.split('.')[1]
            foreign_on_delete = foreign_on_delete.strip(',')
            foreign_key_id[curr_field_name] = [foreign_table_name, foreign_on_delete]

    return foreign_key_id

def get_table_fields(table_name, is_with_foreignkey=1):
    """
    返回一个表里的字段名列表
    """
    from django.db import connection

    cursor = connection.cursor()
    cursor.execute('''PRAGMA table_info(%s)''' % table_name)
    row_list = cursor.fetchall()
    ret = [i[1] for i in row_list]
    print(ret)
    if is_with_foreignkey!=1:
        cursor = connection.cursor()
        cursor.execute('''PRAGMA foreign_key_list(%s)''' % table_name)
        row_list = cursor.fetchall()
        for i in row_list:
            if i[3] in ret:
                ret.remove(i[3])

    print(ret)
    return ret


def get_table_foreignkey_param_using_pragma(table_name, add_real_table_name=0):
    """
            {"user":["User", "CASCADE"], "article":["Article", "SET_NULL"]}'
    """
    foreign_key_id = {}
    if table_name is None or table_name == '':
        return {}
    from django.db import connection


    cursor = connection.cursor()
    cursor.execute('''PRAGMA foreign_key_list(%s)'''%table_name)
    row_list = cursor.fetchall()
    for row in row_list:
        row_dict = {'id': row[0], 'seq': row[1], 'table': row[2], 'from': row[3], 'to': row[4], 'on_update': row[5],
                    'on_delete': row[6], 'match': row[7]}
        if add_real_table_name==1:
            foreign_key_id[row_dict['from']] = [re.sub(r'[^a-zA-Z0-9]', '', row_dict['table'].title()), row_dict['on_delete'], row_dict['table']]
        else:
            foreign_key_id[row_dict['from']] = [re.sub(r'[^a-zA-Z0-9]', '', row_dict['table'].title()), row_dict['on_delete']]

    return foreign_key_id

def get_table_foreignkey_param(table_name, add_real_table_name=0):
    """
        table_name:
        return: {"user":["User", "CASCADE", 'user'], "article":["Article", "SET_NULL"]}'
    """
    import django
    ver = django.get_version()
    major_ver = ver.split('.')[0]
    major_ver=int(major_ver)
    if major_ver<8:
        key_dict = get_table_foreignkey_param_using_pragma(table_name, add_real_table_name)
        for i in list(key_dict.keys()):
            if (len(i)>3) and (i[-3:]=='_id'):
                old_k = key_dict[i]
                del key_dict[i]
                i=i[:-3]
                key_dict[i]=old_k

        for i in list(key_dict.keys()):
            if len(key_dict[i])>=2:
                if key_dict[i][1]=='NO ACTION':
                    key_dict[i][1]='DO_NOTHING'
                elif key_dict[i][1]=='CASCADE':
                    key_dict[i][1]='CASCADE'
                elif key_dict[i][1]=='SET NULL':
                    key_dict[i][1]='SET_NULL'
                #pragma 对于ondelete: "NO ACTION"--> "NO_NOTHING"


        return key_dict
    else:
        return get_models_param_from_inspectdb(table_name, add_real_table_name)

