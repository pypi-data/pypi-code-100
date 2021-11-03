"""Tests for `matatika context use` command"""

from matatika.cli.commands.root import matatika
from tests.cli.test_cli import TestCLI


class TestCLIContextUse(TestCLI):
    """Test wrapper"""

    def test_use(self):
        """Test command with a context name that exists in the contexts file"""

        context_name = 'context1'
        result = self.runner.invoke(matatika, ["context",
                                               "use",
                                               context_name])

        self.assertFalse(result.output)
        self.assertIs(result.exit_code, 0)

    def test_use_invalid_context_name(self):
        """Test command with a context name that does exist in the contexts file"""

        invalid_context_name = "invalid-context-name"
        result = self.runner.invoke(matatika, ["context",
                                               "use",
                                               invalid_context_name])

        msg = f"Context '{invalid_context_name}' does not exist"
        self.assertIn(msg, result.output)
        self.assertIs(result.exit_code, 1)
