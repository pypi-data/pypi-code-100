import logging
from genie.conf.base import Device, Testbed
from genie.libs.parser.utils import get_parser
from genie import parsergen
from pyats.datastructures import AttrDict


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s|%(name)s|%(levelname)s|%(message)s')

sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(formatter)
logger.addHandler(sh)


def test():
    print('test') 


def parse(raw_cli_output, cmd, os, platform=None):
    logger.debug(f'parse called for {cmd} ({os})')

    # create dummy device 
    # supported genie OSes: https://github.com/CiscoTestAutomation/genieparser/tree/master/src/genie/libs/parser
    device = Device("new_device", os=os)
    device.custom.setdefault("abstraction", {})["order"] = ["os"]
    device.cli = AttrDict({"execute": None})

    # available parsers: https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/parsers
    try:
        get_parser(cmd, device)
    except Exception as e:
        logger.error(f'unable to find parser for command {cmd} ({os})')
 
    try:
        return device.parse(cmd, output=raw_cli_output)
    except Exception as e:
        logger.error(f'unable to parse command ouput for {cmd} ({os})')
        logger.error(e)
