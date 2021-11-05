from _pytest.config.argparsing import Parser
from _pytest.fixtures import FixtureRequest
import pytest


def pytest_addoption(parser: Parser) -> None:
    parser.addoption("--local-repo")


@pytest.fixture
def local_repo(request: FixtureRequest) -> str:
    lr = request.config.getoption("--local-repo")
    if lr is None:
        pytest.skip("--local-repo not set")
    assert isinstance(lr, str)
    return lr
