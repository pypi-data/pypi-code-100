"""Tests for `matatika context delete` command"""

from matatika.cli.commands.root import matatika
from tests.cli.test_cli import TestCLI


class TestCLIContextDelete(TestCLI):
    """Test wrapper"""

    def test_delete(self):
        """Test command with a context name that does exist in the contexts file"""

        context_name = 'context1'
        result = self.runner.invoke(matatika, ["context",
                                               "delete",
                                               context_name])

        self.assertNotIn(context_name, self.mock__read_json)
        self.assertFalse(result.output)
        self.assertIs(result.exit_code, 0)

    def test_delete_invalid_context_name(self):
        """Test command with a context name that does not exist in the contexts file"""

        invalid_context_name = "invalid-context-name"
        result = self.runner.invoke(matatika, ["context",
                                               "delete",
                                               invalid_context_name])

        msg = f"Context '{invalid_context_name}' does not exist"
        self.assertIn(msg, result.output)
        self.assertIs(result.exit_code, 1)
