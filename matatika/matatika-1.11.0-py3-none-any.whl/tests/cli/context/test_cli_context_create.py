"""Tests for `matatika context create` command"""

from unittest.mock import patch, Mock
from uuid import uuid4
from matatika.cli.commands.root import matatika
from tests.cli.test_cli import TestCLI


class TestCLIContextCreate(TestCLI):
    """Test wrapper"""

    def test_create_no_context_name_arg(self):
        """Test command without context name argument"""

        result = self.runner.invoke(matatika, ["context",
                                               "create"])

        self.assertIn("Error: Missing argument 'CONTEXT_NAME'.", result.output)
        self.assertIs(result.exit_code, 2)

    def test_create_no_opts(self):
        """Test command with no options specified"""

        context_name = "unittest"

        result = self.runner.invoke(matatika, ["context",
                                               "create",
                                               context_name])

        self.assertIs(result.exit_code, 0)

    @patch('matatika.context.MatatikaContext._read_json')
    def test_create_existing_context_name(self, mock_read_json: Mock):
        """Test command with a context name that already exists"""

        context_name = 'existing-context'

        mock_read_json.return_value = {
            'contexts': {context_name: {}}
        }

        result = self.runner.invoke(matatika, ["context",
                                               "create",
                                               context_name])

        msg = f"Context '{context_name}' already exists"
        self.assertIn(msg, result.output)
        self.assertIs(result.exit_code, 1)

    def test_create_partial_opts(self):
        """Test command with some options specified"""

        context_name = "unittest"
        variables = {
            'auth_token': "auth_token"
        }

        result = self.runner.invoke(matatika, ["context",
                                               "create",
                                               context_name,
                                               "-a", variables['auth_token']])

        self.assertFalse(result.output)
        self.assertIs(result.exit_code, 0)

    def test_create_all_opts(self):
        """Test command with all options specified"""

        context_name = "unittest"
        variables = {
            'auth_token': "auth_token",
            'client_id': "client_id",
            'client_secret': "client_secret",
            'endpoint_url': "endpoint_url",
            'workspace_id': str(uuid4())
        }

        result = self.runner.invoke(matatika, ["context",
                                               "create",
                                               context_name,
                                               "-a", variables['auth_token'],
                                               "-i", variables['client_id'],
                                               "-s", variables['client_secret'],
                                               "-e", variables['endpoint_url'],
                                               "-w", variables['workspace_id']])

        self.assertFalse(result.output)
        self.assertIs(result.exit_code, 0)

    def test_create_workspace_id_not_uuid(self):
        """Test command with an invalid workspace ID value"""

        context_name = "unittest"
        workspace_id = "workspace id"

        result = self.runner.invoke(matatika, ["context",
                                               "create",
                                               context_name,
                                               "-w", workspace_id])

        print(result.output)

        msg = "Error: Invalid value for '--workspace-id' / '-w': " \
            f"{workspace_id} is not a valid UUID value"
        self.assertIn(msg, result.output)
        self.assertIs(result.exit_code, 2)
