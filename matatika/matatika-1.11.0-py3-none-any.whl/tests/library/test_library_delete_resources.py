"""Library 'delete_resources' method test module"""

from unittest.mock import patch
from uuid import uuid4
from matatika.types import Resource
from .test_library import TestLibrary


class TestLibraryDeleteResources(TestLibrary):
    """Test class for library 'delete_resources' method"""

    def setUp(self):

        super().setUp()

        mock_delete = patch('matatika.catalog.requests.Session.delete')
        self.mock_delete = mock_delete.start()

        self.mock_delete.return_value.status_code = 204

        self.addCleanup(mock_delete.stop)

    def test_str_arg_type_invalid(self):
        """Test provided built-in Python type object instances trigger a TypeError"""

        for type_ in {int, float, str, tuple, set, list, dict}:
            type_instance = type_()

            with self.assertRaises(TypeError) as ctx:
                self.client.delete_resources(type_instance)

            error_msg = ctx.exception.__str__()
            print(error_msg)

            self.assertEqual(error_msg,
                             f'Resource argument expected, got {type(type_instance).__name__}')

    def test_delete_workspaces_single(self):
        """Test delete workspaces with a single workspace ID"""

        workspace_id = str(uuid4())
        self.client.delete_resources(Resource.WORKSPACE, workspace_id)

    def test_delete_workspaces_multiple_inline(self):
        """Test delete workspaces with multiple inline workspace IDs"""

        workspace1_id = str(uuid4())
        workspace2_id = str(uuid4())
        workspace3_id = str(uuid4())
        self.client.delete_resources(Resource.WORKSPACE,
                                     workspace1_id,
                                     workspace2_id,
                                     workspace3_id)

    def test_delete_workspaces_multiple_unpacked(self):
        """Test delete workspaces with multiple workspace IDs unpacked from an iterable"""

        workspace_ids = (str(uuid4()), str(uuid4()), str(uuid4()))
        self.client.delete_resources(Resource.WORKSPACE, *workspace_ids)

    def test_delete_datasets_single(self):
        """Test delete datasets with a single dataset ID"""

        dataset_id = str(uuid4())
        self.client.delete_resources(Resource.DATASET, dataset_id)

    def test_delete_datasets_multiple_inline(self):
        """Test delete datasets with multiple inline dataset IDs"""

        dataset1_id = str(uuid4())
        dataset2_id = str(uuid4())
        dataset3_id = str(uuid4())
        self.client.delete_resources(Resource.DATASET,
                                     dataset1_id,
                                     dataset2_id,
                                     dataset3_id)

    def test_delete_datasets_multiple_unpacked(self):
        """Test delete datasets with multiple dataset IDs unpacked from an iterable"""

        dataset_ids = (str(uuid4()), str(uuid4()), str(uuid4()))
        self.client.delete_resources(Resource.DATASET, *dataset_ids)
