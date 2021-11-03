"""Tests for `matatika context list` command"""

from matatika.cli.commands.root import matatika
from matatika.context import CONTEXTS
from tests.cli.test_cli import MOCK_CONTEXTS_JSON, TestCLI


class TestCLIContextList(TestCLI):
    """Test wrapper"""

    def test_list(self):
        """Test command with existing contexts in the contexts file"""

        result = self.runner.invoke(matatika, ["context",
                                               "list"])

        for context_name in MOCK_CONTEXTS_JSON[CONTEXTS]:
            self.assertIn(context_name, result.output)

        self.assertIs(result.exit_code, 0)

    def test_list_no_contexts(self):
        """Test command with no existing contexts in the contexts file"""

        result = self.runner.invoke(matatika, ["context",
                                               "list"])

        self.assertIs(result.exit_code, 0)
