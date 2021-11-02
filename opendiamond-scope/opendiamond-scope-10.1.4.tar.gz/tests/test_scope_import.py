#
#  The OpenDiamond Platform for Interactive Search
#
# SPDX-FileCopyrightText: 2021 Carnegie Mellon University
# SPDX-License-Identifier: EPL-1.0
#

from click.testing import CliRunner

from opendiamond.console.scope import cli


# Test opendiamond-scope import
def test_import_missing_scope_argument():
    runner = CliRunner()

    result = runner.invoke(cli, ["import"])
    assert result.exit_code == 2
    assert "Missing argument" in result.output


def test_import_missing_scope(isolated_runner):
    # try with non-existing scope file
    result = isolated_runner.invoke(cli, ["import", "scope"])
    assert result.exit_code == 2
    assert "File 'scope' does not exist" in result.output
