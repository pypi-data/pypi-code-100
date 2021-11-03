"""Tests for `matatika context info` command"""

from matatika.cli.commands.root import matatika
from matatika.context import DEFAULT, TEMPLATE, CONTEXTS
from tests.cli.test_cli import MOCK_CONTEXTS_JSON, TestCLI


class TestCLIContextInfo(TestCLI):
    """Test wrapper"""

    def test_info(self):
        """Test command with a default context set in the contexts file"""

        result = self.runner.invoke(matatika, ["context",
                                               "info"])

        default_context_name = MOCK_CONTEXTS_JSON[DEFAULT]

        for key, value in MOCK_CONTEXTS_JSON[CONTEXTS][default_context_name].items():
            if key is not 'client_secret':
                self.assertIn(value, result.output)

        self.assertIs(result.exit_code, 0)

    def test_info_no_default_context(self):
        """Test command with no default context set in the contexts file"""

        # override patch return value
        self.mock__read_json.return_value = TEMPLATE

        result = self.runner.invoke(matatika, ["context",
                                               "info"])

        msg = "No default context is set\n" \
            "Set one using 'matatika context use' (see 'matatika context use --help')"
        self.assertIn(msg, result.output)
        self.assertIs(result.exit_code, 1)
