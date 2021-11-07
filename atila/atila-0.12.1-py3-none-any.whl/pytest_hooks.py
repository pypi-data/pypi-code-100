import pytest
from rs4.webkit import apidoc
from rs4 import pathtool
import os

def pytest_addoption (parser):
    parser.addoption (
        "--run-slow", action="store_true", default=False, help="run inckuding slow marked tests"
    )
    parser.addoption (
        "--docs", action='store_true', default=False, help="generate API document ../docs"
    )

def pytest_collection_modifyitems (config, items):
    if config.getoption ("--run-slow"):
        return
    skip_slow = pytest.mark.skip (reason = "need --run-slow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker (skip_slow)

def pytest_sessionstart (session):
    if session.config.getoption ("--docs"):
        apidoc.truncate_log_dir ()

def pytest_sessionfinish (session, exitstatus):
    subdname = session.config.args [0]
    if session.config.args [0] == os.getcwd ():
        subdname = 'index'
    if exitstatus == 0 and session.config.getoption ("--docs"):
        pathtool.mkdir ('../docs/api')
        apidoc.build_doc ('../docs/api/{}.md'.format (subdname))
