"""A tiny xmlparser"""

__version__ = '0.0.1'
__all__ = ['xmlparse', 'errors']

from .errors import MuzzleError  # noqa
from .xmlparse import XMLParser  # noqa
from .xmlparse import XMLNone  # noqa


def parse(content, namespaces={}):
    parser = XMLParser(namespaces=namespaces)
    return parser.parse(content)


def find(xml, path, namespaces={}):
    parser = XMLParser(namespaces=namespaces)
    return parser.find(xml, path)


def findall(xml, path, namespaces={}):
    parser = XMLParser(namespaces=namespaces)
    return parser.findall(xml, path)


def tostring(xml):
    parser = XMLParser()
    return parser.tostring(xml)


def todict(xml, **kwargs):
    params = ['namespaces']
    parser = XMLParser(namespaces=kwargs.get('namespaces', {}))
    dict_args = {k: v for k, v in kwargs.items() if k not in params}
    return parser.todict(xml, **dict_args)
