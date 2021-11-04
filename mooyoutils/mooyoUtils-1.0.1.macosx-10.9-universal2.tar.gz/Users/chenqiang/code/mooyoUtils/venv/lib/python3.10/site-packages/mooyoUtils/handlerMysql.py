# -*- coding: UTF-8 -*-
# @Time     : 2020/8/27 11:00
# @Author   : Jackie
# @File     : handlerMysql.py

import pymysql

from .read_config import apollo_reader
from .logger import logger


class MyDB:
    def __init__(self, database='default'):
        apollo_configurations = apollo_reader.get_configurations()
        mysql_hosts = [key for key in apollo_configurations.keys() if key.startswith('mysql') and key.endswith('host')]
        databases = [database.split('.')[1] for database in mysql_hosts]

        self.database = database
        if self.database not in databases:
            self.database = 'default'

        db_config = {
            'host': apollo_reader.get_value('mysql.%s.host' % str(self.database)),
            'user': apollo_reader.get_value('mysql.%s.user' % str(self.database)),
            'passwd': apollo_reader.get_value('mysql.%s.pwd' % str(self.database)),
            'port': int(apollo_reader.get_value('mysql.%s.port' % str(self.database))),
            'db': apollo_reader.get_value('mysql.%s.database' % str(self.database)),
        }

        self.db = pymysql.connect(**db_config)
        self.cursor = self.db.cursor()
        self.cursor_dict = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    def execute_sql(self, sql, is_dict=False, is_commit=True):
        self.ping()
        if is_dict:
            self.cursor_dict.execute(sql)
            cursor = self.cursor_dict
        else:
            self.cursor.execute(sql)
            cursor = self.cursor
        if is_commit:
            self.db.commit()
        return cursor

    def get_all(self, is_dict=False):
        if is_dict:
            value = self.cursor_dict.fetchall()
        else:
            value = self.cursor.fetchall()
        return value

    def get_one(self):
        value = self.cursor.fetchone()
        if value is not None:
            try:
                return value[0]
            except IndexError:
                return None
        return value

    def commit(self):
        self.db.commit()

    def ping(self, reconnect=True):
        self.db.ping(reconnect)

    def close_db(self):
        self.db.close()
        logger.info("Database closed!")
