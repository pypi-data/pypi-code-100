import logging
import os
import tempfile

import pytest

import handypy.utils as utils


def test_validate_folder():
    with tempfile.NamedTemporaryFile() as f:
        with pytest.raises(FileExistsError):
            utils.validate_folder(f.name)

    with tempfile.TemporaryDirectory() as f:
        utils.validate_folder(f)
        utils.validate_folder(f + "/test")
        assert os.path.isdir(f + '/test'), "Fail to create folder"


def test_load_yaml_namespace():
    config = """a: 3"""
    f = tempfile.NamedTemporaryFile()
    with open(f.name, 'w') as fp:
        fp.write(config)

    z = utils.load_yaml_namespace(f.name)
    assert z.a == 3, "yaml failed"
    f.close()


def test_set_log():
    utils.set_log("info")
    utils.set_log("error")
    utils.set_log("unknown")
    logging.info("finished")
