from configparser import ConfigParser
import configparser
from .db import getPath

config = ConfigParser()
path = getPath('setting.ini')

config.read(path)

__all__ = [
    'getConfig',
    'setConfig',
    'setSection'
]


def __callback(func):
    def inner(*args):
        try:
            return func(*args)
        except configparser.DuplicateSectionError:
           return None; 
        except configparser.NoSectionError:
            setSection(args[0])
        except configparser.NoOptionError:
            setConfig(args[0],args[1],'')

        return func(*args)
    return inner

@__callback
def getConfig(section:str, key:str):
    return config.get(section, key)

@__callback
def setConfig(section:str, key:str,value:str):
    config.set(section, key,value)
    __write()

@__callback
def setSection(section:str):
    config.add_section(section)
    __write()


def __write():
    with open(path, 'w') as f:
        config.write(f)