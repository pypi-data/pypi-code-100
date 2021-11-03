"""CLI 'delete' command test module"""

# standard
from unittest.mock import patch, Mock
from uuid import uuid4
# pip
from requests.models import Response
# local
from matatika.cli.commands.root import matatika
from tests.cli.test_cli import TestCLI


class TestCLIDelete(TestCLI):
    """Test class for CLI delete command"""

    def test_delete_no_subcommand(self):
        """Test delete with no subcommand"""

        result = self.runner.invoke(matatika, ["delete"])

        expected_message = "Usage: matatika delete [OPTIONS] COMMAND [ARGS]..."
        self.assertIn(expected_message, result.output)

        self.assertIs(result.exit_code, 0)

    def test_delete_invalid_subcommand(self):
        """Test delete with an invalid subcommand"""

        resource_type = "invalid-resource-type"

        result = self.runner.invoke(matatika, ["delete", resource_type])

        expected_message = f"Error: No such command '{resource_type}'."
        self.assertIn(expected_message, result.output)

        self.assertIs(result.exit_code, 2)


class TestCLIDeleteWorkspace(TestCLI):
    """Test class for CLI delete workspaces command"""

    def test_delete_workspaces_no_arguments(self):
        """Test command error when no workspace ID arguments are not provided"""

        result = self.runner.invoke(matatika, ["delete",
                                               "workspaces"])

        expected_message = "Missing argument 'WORKSPACE_IDS...'"
        self.assertIn(expected_message, result.output)

    def test_delete_workspaces_confirm_no(self):
        """Test workspace is not deleted after rejected client confirmation"""

        workspace_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "workspaces",
                                               workspace_id], input='n')

        expected_message = "This action cannot be undone. Do you want to continue? [y/N]: n"
        self.assertEqual(result.output.strip('\n'), expected_message)

        self.assertIs(result.exit_code, 0)

    @patch('matatika.catalog.requests.Session.delete')
    def test_delete_workspaces_confirm_yes(self, mock_delete_request: Mock):
        """Test workspace is deleted after client confirmation"""

        mock_delete_request.return_value.status_code = 204

        workspace_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "workspaces",
                                               workspace_id], input='y')

        expected_message = "This action cannot be undone. Do you want to continue? [y/N]: y"
        self.assertIn(expected_message, result.output)

        expected_message = f"Successfully deleted workspace(s): {workspace_id}"
        self.assertIn(expected_message, result.output)

        self.assertIs(result.exit_code, 0)

    @patch('matatika.catalog.requests.Session.delete')
    def test_delete_workspaces_bypass_confirm(self, mock_delete_request: Mock):
        """Test workspace is deleted with no client confirmation"""

        mock_delete_request.return_value.status_code = 204

        workspace_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "--bypass-confirm",
                                               "workspaces",
                                               workspace_id])

        expected_message = f"Successfully deleted workspace(s): {workspace_id}"
        self.assertEqual(result.output.strip('\n'), expected_message)

        self.assertIs(result.exit_code, 0)

    @patch('matatika.catalog.requests.Session.delete')
    def test_delete_workspaces_not_found(self, mock_delete_request: Mock):
        """Test workspace is not found when trying to delete"""

        mock_delete_request.return_value.status_code = 404

        workspace_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "workspaces",
                                               workspace_id], input='y')

        expected_message = f"Workspace {workspace_id} does not exist within the current " \
            "authorisation context"
        self.assertIn(expected_message, result.output)

    @patch('matatika.catalog.requests.Session.delete')
    def test_delete_workspaces_server_error(self, mock_delete_request: Mock):
        """Test server error encountered when trying to delete workspace"""

        mock_response = Response()
        mock_response.status_code = 503
        mock_delete_request.return_value = mock_response

        workspace_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "workspaces",
                                               workspace_id], input='y')

        expected_message = f"{mock_response.status_code} Server Error"
        self.assertIn(expected_message, result.output)

    @patch('matatika.catalog.requests.Session.delete')
    def test_delete_workspaces_multiple(self, mock_delete_request: Mock):
        """Test delete of multiple workspaces"""

        mock_delete_request.return_value.status_code = 204

        workspace1_id = str(uuid4())
        workspace2_id = str(uuid4())
        workspace3_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "--bypass-confirm",
                                               "workspaces",
                                               workspace1_id,
                                               workspace2_id,
                                               workspace3_id])

        expected_message = "Successfully deleted workspace(s): " \
            f"{workspace1_id}, {workspace2_id}, {workspace3_id}"
        self.assertEqual(result.output.strip('\n'), expected_message)

        self.assertIs(result.exit_code, 0)


class TestCLIDeleteDataset(TestCLI):
    """Test class for CLI delete dataset command"""

    def test_delete_datasets_no_arguments(self):
        """Test command error when no dataset ID arguments are not provided"""

        result = self.runner.invoke(matatika, ["delete",
                                               "datasets"])

        expected_message = "Missing argument 'DATASET_IDS...'"
        self.assertIn(expected_message, result.output)
        self.assertIs(result.exit_code, 2)

    def test_delete_datasets_confirm_no(self):
        """Test dataset is not deleted after rejected client confirmation"""

        dataset_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "datasets",
                                               dataset_id], input='n')

        expected_message = "This action cannot be undone. Do you want to continue? [y/N]: n"
        self.assertEqual(result.output.strip('\n'), expected_message)

        self.assertIs(result.exit_code, 0)

    @patch('matatika.catalog.requests.Session.delete')
    def test_delete_datasets_confirm_yes(self, mock_delete_request: Mock):
        """Test dataset is deleted after client confirmation"""

        mock_delete_request.return_value.status_code = 204

        dataset_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "datasets",
                                               dataset_id], input='y')

        expected_message = "This action cannot be undone. Do you want to continue? [y/N]: y"
        self.assertIn(expected_message, result.output)

        expected_message = f"Successfully deleted dataset(s): {dataset_id}"
        self.assertIn(expected_message, result.output)

        self.assertIs(result.exit_code, 0)

    @patch('matatika.catalog.requests.Session.delete')
    def test_delete_datasets_bypass_confirm(self, mock_delete_request: Mock):
        """Test dataset is deleted with no client confirmation"""

        mock_delete_request.return_value.status_code = 204

        dataset_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "--bypass-confirm",
                                               "datasets",
                                               dataset_id])

        expected_message = f"Successfully deleted dataset(s): {dataset_id}"
        self.assertEqual(result.output.strip('\n'), expected_message)

        self.assertIs(result.exit_code, 0)

    @patch('matatika.catalog.requests.Session.delete')
    def test_delete_datasets_not_found(self, mock_delete_request: Mock):
        """Test dataset is not found when trying to delete"""

        mock_delete_request.return_value.status_code = 404

        dataset_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "datasets",
                                               dataset_id], input='y')

        expected_message = f"Dataset {dataset_id} does not exist within the current " \
            "authorisation context"
        self.assertIn(expected_message, result.output)

    @patch('matatika.catalog.requests.Session.delete')
    def test_delete_datasets_server_error(self, mock_delete_request: Mock):
        """Test server error encountered when trying to delete dataset"""

        mock_response = Response()
        mock_response.status_code = 503
        mock_delete_request.return_value = mock_response

        dataset_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "datasets",
                                               dataset_id], input='y')

        expected_message = f"{mock_response.status_code} Server Error"
        self.assertIn(expected_message, result.output)

    @patch('matatika.catalog.requests.Session.delete')
    def test_delete_datasets_multiple(self, mock_delete_request: Mock):
        """Test delete of multiple datasets"""

        mock_delete_request.return_value.status_code = 204

        dataset1_id = str(uuid4())
        dataset2_id = str(uuid4())
        dataset3_id = str(uuid4())

        result = self.runner.invoke(matatika, ["delete",
                                               "--bypass-confirm",
                                               "datasets",
                                               dataset1_id,
                                               dataset2_id,
                                               dataset3_id])

        expected_message = "Successfully deleted dataset(s): " \
            f"{dataset1_id}, {dataset2_id}, {dataset3_id}"
        self.assertEqual(result.output.strip('\n'), expected_message)

        self.assertIs(result.exit_code, 0)
