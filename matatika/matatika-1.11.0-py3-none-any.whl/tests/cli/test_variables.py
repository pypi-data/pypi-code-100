"""Tests for variables"""

import os
from unittest import TestCase
from unittest.mock import patch
from click.core import Command, Context
from matatika.cli.variables import (
    AuthTokenVariable,
    ClientIdVariable,
    ClientSecretVariable,
    EndpointUrlVariable,
    WorkspaceIdVariable,
    VariableSource
)
from matatika.context import CONTEXTS, DEFAULT

MOCK_ENV = {
    'AUTH_TOKEN': 'env_auth_token',
    'CLIENT_ID': 'env_client_id',
    'CLIENT_SECRET': 'env_client_secret',
    'ENDPOINT_URL': 'env_endpoint_url',
    'WORKSPACE_ID': 'env_workspace_id'
}

MOCK_COMMAND = {
    'auth_token': 'command_auth_token',
    'client_id': 'command_client_id',
    'client_secret': 'command_client_secret',
    'endpoint_url': 'command_endpoint_url',
    'workspace_id': 'command_workspace_id'
}

MOCK_CONTEXTS = {
    'default': 'test',
    'contexts': {
        'test': {
            'auth_token': 'context_auth_token',
            'client_id': 'context_client_id',
            'client_secret': 'context_client_secret',
            'endpoint_url': 'context_endpoint_url',
            'workspace_id': 'context_workspace_id'
        }
    }
}


class TestVariables(TestCase):
    """Test wrapper"""

    def setUp(self):
        self.variables = (
            AuthTokenVariable(),
            ClientIdVariable(),
            ClientSecretVariable(),
            EndpointUrlVariable(),
            WorkspaceIdVariable()
        )

        self.ctx = Context(Command('test'))
        self.ctx.ensure_object(dict)

    def test_variables_from_command(self):
        """Test variables are resolved from the command"""
        self.ctx.obj.update(MOCK_COMMAND)

        for variable in self.variables:
            value, source = variable.get(self.ctx)

            self.assertEqual(MOCK_COMMAND[variable.name.lower()], value)
            self.assertEqual(VariableSource.COMMAND, source)

    @patch('matatika.context.MatatikaContext._read_json')
    def test_variables_from_context(self, mock_read_json):
        """Test variables are resolved from `contexts.json`"""

        mock_read_json.return_value = MOCK_CONTEXTS
        default = MOCK_CONTEXTS['default']

        for variable in self.variables:
            value, source = variable.get(self.ctx)

            variable_name = variable.name.lower()
            context_value = MOCK_CONTEXTS[CONTEXTS][default][variable_name]
            self.assertEqual(context_value, value)
            self.assertEqual(VariableSource.CONTEXT, source)

    @patch.dict(os.environ, MOCK_ENV)
    def test_variables_from_env(self):
        """Test variables are resolved from the system environment"""

        for variable in self.variables:
            value, source = variable.get(self.ctx)

            self.assertEqual(MOCK_ENV[variable.name], value)
            self.assertEqual(VariableSource.ENV, source)

    @patch('matatika.context.MatatikaContext._read_json', return_value=MOCK_CONTEXTS)
    def test_variable_resolution_heirarchy(self, _mock_read_json):
        """Test variables are resolved according to the defined heirarchy"""

        mock_command = {
            'auth_token': 'command_auth_token',
            'endpoint_url': 'command_endpoint_url'
        }
        self.ctx.obj.update(mock_command)

        mock_env = {
            'AUTH_TOKEN': 'env_auth_token',
            'CLIENT_SECRET': 'env_client_secret'
        }

        default_context = MOCK_CONTEXTS[CONTEXTS][MOCK_CONTEXTS[DEFAULT]]

        with patch.dict(os.environ, mock_env):
            for variable in self.variables:
                value, source = variable.get(self.ctx)

                command_value = self.ctx.obj.get(variable.name.lower())
                env_value = mock_env.get(variable.name)
                context_value = default_context.get(variable.name.lower())

                if isinstance(variable, AuthTokenVariable):
                    self.assertEqual(command_value, value)
                    self.assertEqual(VariableSource.COMMAND, source)

                elif isinstance(variable, EndpointUrlVariable):
                    self.assertEqual(command_value, value)
                    self.assertEqual(VariableSource.COMMAND, source)

                elif isinstance(variable, ClientSecretVariable):
                    self.assertEqual(env_value, value)
                    self.assertEqual(VariableSource.ENV, source)

                else:
                    self.assertEqual(context_value, value)
                    self.assertEqual(VariableSource.CONTEXT, source)
