import pytest
from click.testing import CliRunner

import flowingo.__main__


@pytest.fixture(scope="module")
def cli_runner():
    return CliRunner()
