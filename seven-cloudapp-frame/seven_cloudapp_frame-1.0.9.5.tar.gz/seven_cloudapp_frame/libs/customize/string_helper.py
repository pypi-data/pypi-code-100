# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2021-10-22 13:32:07
@LastEditTime: 2021-10-22 13:44:10
@LastEditors: HuangJianYi
@Description: 
"""
import re

class StringHelper:
    """
    :description: 字符串帮助类
    """

    #sql关键字
    _sql_pattern = r"\b(and|like|exec|execute|insert|select|drop|grant|alter|delete|update|count|chr|mid|limit|substring|restore|xp_cmdshell|master|backup|truncate|char|delclare|or)\b|(\*|;)"

    @classmethod
    def is_contain_sql(self, str):
        """
            :description: 是否包含sql关键字
            :param str:参数值
            :return:
            :last_editors: HuangJianYi
            """
        result = re.search(self._sql_pattern, str.lower())
        if result:
            return True
        else:
            return False

    @classmethod
    def filter_sql(self, str):
        """
        :description: 过滤sql关键字
        :param str:参数值
        :return:
        :last_editors: HuangJianYi
        """
        result = re.findall(self._sql_pattern, str.lower())
        for item in result:
            str = str.replace(item[0], "")
            str = str.replace(item[0].upper(), "")
        return str

    @classmethod
    def filter_sql_special_key(self, str):
        """
        :description: 过滤sql特殊字符
        :param str:参数值
        :return:
        :last_editors: HuangJianYi
        """
        special_key_list = ["\"", "\\", "/", "*", "'", "=", "-", "#", ";", "<", ">", "+", "%", "$", "(", ")", "%", "@","!"]
        for item in special_key_list:
            str = str.replace(item, "")
        return str
