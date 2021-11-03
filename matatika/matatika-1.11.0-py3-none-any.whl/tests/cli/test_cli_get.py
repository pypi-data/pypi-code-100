"""CLI 'list' command test module"""

# standard
import json
from unittest.mock import patch
from uuid import uuid4
# local
from matatika.cli.commands.root import matatika
from matatika.context import CONTEXTS
from matatika.exceptions import VariableNotSetError
from tests.cli.test_cli import TestCLI
from tests.api_response_mocks import DATASET


class TestCLIGet(TestCLI):
    """Test class for CLI get command"""

    def test_get_no_subcommmand(self):
        """Test get with no subcommand"""

        result = self.runner.invoke(matatika, ["get"])
        self.assertIn(
            "Usage: matatika get [OPTIONS] COMMAND [ARGS]...", result.output)
        self.assertIs(result.exit_code, 0)

    def test_get_invalid_subcommand(self):
        """Test get with an invalid subcommand"""

        resource_type = "invalid-resource-type"

        result = self.runner.invoke(matatika, ["get", resource_type])
        self.assertIn(
            f"Error: No such command '{resource_type}'.", result.output)
        self.assertIs(result.exit_code, 2)

    @patch('matatika.catalog.requests.Session.get')
    def test_get_dataset_by_id(self, mock_get_request):
        """Test get dataset by ID"""

        mock_get_request.return_value.status_code = 200
        mock_get_request.return_value.json.return_value = DATASET

        result = self.runner.invoke(matatika, ["get",
                                               "dataset",
                                               str(uuid4())])

        self.assertIn(json.dumps(DATASET), result.output)

    @patch('matatika.catalog.requests.Session.get')
    def test_get_dataset_by_alias(self, mock_get_request):
        """Test get dataset by alias"""

        mock_get_request.return_value.status_code = 200
        mock_get_request.return_value.json.return_value = DATASET

        result = self.runner.invoke(matatika, ["get",
                                               "dataset",
                                               "alias",
                                               "-w",
                                               str(uuid4())])

        self.assertIn(json.dumps(DATASET), result.output)

    def test_get_dataset_by_alias_no_workspace_id(self):
        """Test get dataset by alias without specifying a workspace ID"""

        self.mock__read_json.return_value[CONTEXTS]['context1']['workspace_id'] = None

        workspace_id_not_set_msg = str(VariableNotSetError('WORKSPACE_ID'))

        invalid_alias = 'invalid-alias'
        result = self.runner.invoke(matatika, ["get",
                                               "dataset",
                                               invalid_alias])
        self.assertIn(workspace_id_not_set_msg, result.output)

    @patch('matatika.catalog.requests.Session.get')
    def test_get_dataset_by_invalid_alias(self, mock_get_request):
        """Test get dataset by an invalid dataset alias"""

        mock_get_request.return_value.status_code = 404

        invalid_alias = 'invalid-alias'
        result = self.runner.invoke(matatika, ["get",
                                               "dataset",
                                               invalid_alias,
                                               "-w",
                                               str(uuid4())])
        self.assertIn(
            f"Dataset {invalid_alias} does not exist within the current authorisation context",
            result.output)
