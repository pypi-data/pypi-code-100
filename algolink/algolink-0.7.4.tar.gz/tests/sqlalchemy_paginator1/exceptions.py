"""
Created on Oct 30, 2021
@author: leepand6@gmail.com
"""


class InvalidPage(Exception):
    pass


class PageNotAnInteger(InvalidPage):
    pass


class EmptyPage(InvalidPage):
    pass
