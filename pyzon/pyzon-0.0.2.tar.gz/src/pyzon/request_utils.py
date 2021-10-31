# -*- coding: utf-8 -*-
# @Time    : 5/22/2021 2:11 AM
# @Author  : nzooherd
# @File    : request_utils.py
# @Software: PyCharm
from typing import Dict


def format_cookies(cookies: str) -> Dict[str, str]:
    return  {item[0]: item[1] for item in  map(lambda cookie_str: cookie_str.rstrip().split("=") ,cookies.split(";"))}

