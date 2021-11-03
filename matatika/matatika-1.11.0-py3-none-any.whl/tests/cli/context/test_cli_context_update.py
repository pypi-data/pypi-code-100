"""Tests for `matatika context update` command"""

from uuid import uuid4
from matatika.cli.commands.root import matatika
from matatika.context import TEMPLATE
from tests.cli.test_cli import TestCLI


class TestCLIContextUpdate(TestCLI):
    """Test wrapper"""

    def test_update_no_default_context(self):
        """Test command with no default context set in the contexts file"""

        # override patch return value
        self.mock__read_json.return_value = TEMPLATE

        result = self.runner.invoke(matatika, ["context",
                                               "update"])

        msg = "No default context is set\n" \
            "Set one using 'matatika context use' (see 'matatika context use --help')"
        self.assertIn(msg, result.output)
        self.assertIs(result.exit_code, 1)

    def test_update_no_opts(self):
        """Test command with no options specified"""

        result = self.runner.invoke(matatika, ["context",
                                               "update"])

        self.assertFalse(result.output)
        self.assertIs(result.exit_code, 0)

    def test_update_partial_opts(self):
        """Test command with some options specified"""

        variables = {
            'auth_token': "auth_token"
        }

        result = self.runner.invoke(matatika, ["context",
                                               "update",
                                               "-a", variables['auth_token']])

        self.assertFalse(result.output)
        self.assertIs(result.exit_code, 0)

    def test_update_all_opts(self):
        """Test command with all options specified"""

        variables = {
            'auth_token': "auth_token",
            'client_id': "client_id",
            'client_secret': "client_secret",
            'endpoint_url': "endpoint_url",
            'workspace_id': str(uuid4())
        }

        result = self.runner.invoke(matatika, ["context",
                                               "update",
                                               "-a", variables['auth_token'],
                                               "-i", variables['client_id'],
                                               "-s", variables['client_secret'],
                                               "-e", variables['endpoint_url'],
                                               "-w", variables['workspace_id']])

        self.assertFalse(result.output)
        self.assertIs(result.exit_code, 0)

    def test_update_workspace_id_not_uuid(self):
        """Test command with an invalid workspace ID value"""

        context_name = "unittest"
        workspace_id = "workspace id"

        result = self.runner.invoke(matatika, ["context",
                                               "update",
                                               context_name,
                                               "-w", workspace_id])

        print(result.output)

        self.assertIn(
            "Error: Invalid value for '--workspace-id' / '-w':", result.output)
        self.assertIn(
            f"{workspace_id} is not a valid UUID value", result.output)
        self.assertIs(result.exit_code, 2)
