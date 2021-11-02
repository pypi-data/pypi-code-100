#
#  The OpenDiamond Platform for Interactive Search
#
# SPDX-FileCopyrightText: 2021 Carnegie Mellon University
# SPDX-License-Identifier: EPL-1.0
#

import pytest
from click.testing import CliRunner


@pytest.fixture(scope="module")
def isolated_runner():
    runner = CliRunner()
    with runner.isolated_filesystem():
        yield runner
