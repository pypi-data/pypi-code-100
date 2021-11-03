"""library module"""

# standard
import json
from typing import List, Tuple, Union
# local
from matatika.catalog import Catalog
from matatika.channel import Channel
from matatika import chartjs
from matatika.dataset import Dataset
from matatika.exceptions import MatatikaException
from matatika.metadata import ChartJSMetadata
from matatika.types import DataFormat, Resource
from matatika.utility import is_uuid4


class MatatikaClient():
    """
    Class to handle client context

    Args:
        auth_token (str): Authentication token
        client_id (str): Client ID
        client_secret (str): Client secret
        endpoint_url (str): Endpoint URL
        workspace_id (str): Workspace ID

    Example:

    Create a client with an access token
    ```py
    # create 'auth_token' variable

    client = MatatikaClient(auth_token)
    ```

    Create a client with client credentials
    ```py
    # create 'client_id' and 'client_secret' variables

    client = MatatikaClient(client_id=client_id, client_secret=client_secret)
    ```

    Create a client with an alternate API endpoint URL
    ```py
    # create 'auth_token' and 'endpoint_url' variables

    client = MatatikaClient(auth_token, endpoint_url=endpoint_url)
    ```

    Create a client with a target workspace
    ```py
    # create 'auth_token' and 'workspace_id' variables

    client = MatatikaClient(auth_token, workspace_id=workspace_id)
    ```
    """

    _from_cli = False

    # pylint: disable=too-many-arguments
    def __init__(self,
                 auth_token: str = None,
                 client_id: str = None,
                 client_secret: str = None,
                 endpoint_url: str = 'https://catalog.matatika.com/api',
                 workspace_id: str = None):

        if not (auth_token or (client_id and client_secret)):
            raise ValueError(
                "An access token or client credentials must be provided")

        self._auth_token = auth_token
        self._client_id = client_id
        self._client_secret = client_secret
        self._endpoint_url = endpoint_url
        self._workspace_id = workspace_id

    # getter methods
    @property
    def auth_token(self) -> str:
        """
        Gets the client auth token

        Returns:
            str: Client auth token

        Example:

        ```py
        # create MatatikaClient object

        auth_token = client.auth_token
        print(auth_token)
        ```
        """

        return self._auth_token

    @property
    def client_id(self) -> str:
        """
        Gets the client ID

        Returns:
            str: Client ID

        Example:

        ```py
        # create MatatikaClient object

        client_id = client.client_id
        print(client_id)
        ```
        """

        return self._client_id

    @property
    def client_secret(self) -> str:
        """
        Gets the client secret

        Returns:
            str: Client secret

        Example:

        ```py
        # create MatatikaClient object

        client_secret = client.client_secret
        print(client_secret)
        ```
        """

        return self._client_secret

    @property
    def endpoint_url(self) -> str:
        """
        Gets the client endpoint URL

        Returns:
            str: Client endpoint URL

        Example:

        ```py
        # create MatatikaClient object

        endpoint_url = client.endpoint_url
        print(endpoint_url)
        ```
        """

        return self._endpoint_url

    @property
    def workspace_id(self) -> str:
        """
        Gets the client workspace URL

        Returns:
            str: Client workspace URL

        Example:

        ```py
        # create MatatikaClient object

        workspace_id = client.workspace_id
        print(workspace_id)
        ```
        """

        return self._workspace_id

    # setter methods
    @auth_token.setter
    def auth_token(self, value: str):
        """
        Sets the client authentication token

        Args:
            value (str): Authentication token

        Example:

        ```py
        # create MatatikaClient object
        # create 'auth_token' variable

        client.auth_token = auth_token
        print(client.auth_token)
        ```
        """

        self._auth_token = value

    @client_id.setter
    def client_id(self, value: str):
        """
        Sets the client ID

        Args:
            value (str): Client ID

        Example:

        ```py
        # create MatatikaClient object
        # create 'client_id' variable

        client.client_id = client_id
        print(client.client_id)
        ```
        """

        self._client_id = value

    @client_secret.setter
    def client_secret(self, value: str):
        """
        Sets the client secret

        Args:
            value (str): Client secret

        Example:

        ```py
        # create MatatikaClient object
        # create 'client_secret' variable

        client.client_secret = client_secret
        print(client.client_secret)
        ```
        """

        self._client_secret = value

    @endpoint_url.setter
    def endpoint_url(self, value: str):
        """
        Sets the client endpoint URL

        Args:
            value (str): Endpoint URL

        Example:

        ```py
        # create MatatikaClient object
        # create 'endpoint_url' variable

        client.endpoint_url = endpoint_url
        print(client.endpoint_url)
        ```
        """

        self._endpoint_url = value

    @workspace_id.setter
    def workspace_id(self, value: str):
        """
        Sets the client workspace ID

        Args:
            value (str): Workspace ID

        Example:

        ```py
        # create MatatikaClient object
        # create 'workspace_id' variable

        client.workspace_id = workspace_id
        print(client.workspace_id)
        ```
        """

        self._workspace_id = value

    def profile(self) -> dict:
        """
        Gets the authenticated user profile

        Returns:
            dict: Authenticated user profile

        Example:

        ```py
        # create MatatikaClient object

        profile = client.profile()

        print(profile['id'])
        print(profile['name'])
        print(profile['email'])
        ```
        """

        catalog = Catalog(self)
        return catalog.get_profile()

    def publish(self, resource_type, resources: List[object]) -> List[Tuple[object, int]]:
        """
        Publishes objects
        Args:
            objects (List[object]): objects to publish
        Returns:
            List[Tuple[object,int]]: Published objects and status actions
        Example:
        ```py
        # create MatatikaClient object
        # create 'objects' variable
        responses = client.publish(objects)
        for object, status_code in responses:
            print(
                f"[{status_code}]\tSuccessfully published the object {object.object_id}")
        ```
        """

        catalog = Catalog(self)
        responses = catalog.post_resources(resources)

        published_resources = []

        for response in responses:
            if resource_type == Resource.DATASET:
                resource = Dataset.from_dict(response.json())
            elif resource_type == Resource.CHANNEL:
                resource = Channel.from_dict(response.json())
            published_resources.append((resource, response.status_code))

        return published_resources

    def list_resources(self, resource: Resource) -> Union[list, None]:
        """
        Lists all available resources of the specified type

        Args:
            resource_type (Resource): Resource type to return (workspaces/datasets)

        Returns:
            Union[list,None]: Available resources

        Examples:

        List all workspaces
        ```py
        # create MatatikaClient object

        from matatika.types import Resource

        workspaces = client.list_resources(Resource.WORKSPACE)

        for workspace in workspaces:
            print(workspace['id'], workspace['name'], workspace['domains'])
        ```

        List all datasets in the workspace provided upon client object instantiation
        ```py
        # create MatatikaClient object

        from matatika.types import Resource

        datasets = client.list_resources(Resource.DATASET)

        for dataset in datasets:
            print(dataset['id'], dataset['alias'], dataset['title'])
        ```

        List all datasets in the workspace 'c6db37fd-df5e-4ac6-8824-a4608932bda0'
        ```py
        # create MatatikaClient object

        client.workspace_id = '8566fe13-f30b-4536-aecf-b3879bd0910f'
        datasets = client.list_resources('datasets')

        for dataset in datasets:
            print(dataset['id'], dataset['alias'], dataset['title'])
        ```
        """

        catalog = Catalog(self)

        if not isinstance(resource, Resource):
            raise TypeError(
                f"{Resource.__name__} argument expected, got {type(resource).__name__}")

        if resource == Resource.WORKSPACE:
            return catalog.get_workspaces()

        if resource == Resource.DATASET:
            return catalog.get_datasets()

        if resource == Resource.CHANNEL:
            return catalog.get_channels()

        return None

    def delete_resources(self, resource_type: Resource, *resource_ids) -> None:
        """
        Deletes a resource of the specified type

        Args:
            resource_type (Resource): Resource type to delete (dataset)
            resource_id (str): Resource ID

        Returns:
            None

        Examples:
        Delete a workspace
        ```py
        # create MatatikaClient object
        # create 'workspace_id' variable

        from matatika.types import Resource

        client.delete_resources(Resource.WORKSPACE, workspace_id)
        print(f"Successfully deleted workspace {workspace_id}")
        ```

        Delete multiple workspaces
        ```py
        # create MatatikaClient object
        # create 'workspace1_id', 'workspace2_id' and 'workspace3_id' variables

        from matatika.types import Resource

        client.delete_resources(Resource.WORKSPACE, workspace1_id, workspace2_id, workspace3_id)
        print(f"Successfully deleted workspaces: {workspace1_id}, {workspace2_id}, {workspace3_id}")
        ```

        Delete a dataset
        ```py
        # create MatatikaClient object
        # create 'dataset_id' variable

        from matatika.types import Resource

        client.delete_resources(Resource.DATASET, dataset_id)
        print(f"Successfully deleted dataset {dataset_id}")
        ```

        Delete multiple datasets
        ```py
        # create MatatikaClient object
        # create 'dataset1_id', 'dataset2_id' and 'dataset3_id' variables

        from matatika.types import Resource

        client.delete_resources(Resource.DATASET, dataset1_id, dataset2_id, dataset3_id)
        print(f"Successfully deleted datasets: {dataset1_id}, {dataset2_id}, {dataset3_id}")
        ```
        """

        if not isinstance(resource_type, Resource):
            raise TypeError(
                f"{Resource.__name__} argument expected, got {type(resource_type).__name__}")

        catalog = Catalog(self)

        resource_id: str
        for resource_id in resource_ids:

            if resource_type == Resource.WORKSPACE:
                catalog.delete_workspace(resource_id)

            elif resource_type == Resource.DATASET:
                catalog.delete_dataset(resource_id)

    def fetch(self, dataset_id_or_alias: str, data_format: DataFormat = None) \
            -> Union[dict, list, str]:
        """
        Fetches the data of a dataset using the query property

        Args:
            dataset_id_or_alias (str): Dataset ID or alias
            data_format (DataFormat, optional): Format to return the data as
            (defaults to a native Python object)

        Returns:
            Union[dict,list,str]: Dataset data

        Examples:

        Fetch data as a native Python object
        ```py
        # create MatatikaClient object
        # create 'dataset_id_or_alias' variable

        data = client.fetch(dataset_id_or_alias)

        if data:
            print(data)
        else:
            print(f"No data was found for dataset {dataset_id_or_alias}")
        ```

        Fetch data as a raw string
        ```py
        # create MatatikaClient object
        # create 'dataset_id_or_alias' variable

        from matatika.types import DataFormat

        data = client.fetch(dataset_id_or_alias, data_format=DataFormat.RAW)

        if data:
            print(data)
        else:
            print(f"No data was found for dataset {dataset_id_or_alias}")
        ```

        Fetch data formatted as per the Chart.js specification
        ```py
        # create MatatikaClient object
        # create 'dataset_id_or_alias' variable

        from matatika.types import DataFormat

        data = client.fetch(dataset_id_or_alias,
                            data_format=DataFormat.CHARTJS)

        if data:
            print(data)
        else:
            print(f"No data was found for dataset {dataset_id_or_alias}")
        ```

        Fetch data in CSV format
        ```py
        # create MatatikaClient object
        # create 'dataset_id_or_alias' variable

        from matatika.types import DataFormat

        data = client.fetch(dataset_id_or_alias, data_format=DataFormat.CSV)

        if data:
            print(data)
        else:
            print(f"No data was found for dataset {dataset_id_or_alias}")
        ```
        """

        if data_format is not None and not isinstance(data_format, DataFormat):
            raise TypeError(
                f"{DataFormat.__name__} argument expected, got {type(data_format).__name__}")

        catalog = Catalog(self)

        if is_uuid4(dataset_id_or_alias):
            dataset_json = catalog.get_dataset(dataset_id_or_alias)

        else:
            if not self.workspace_id:
                raise MatatikaException(
                    "Workspace ID must be provided to fetch data by dataset alias")

            dataset_json = catalog.get_workspace_dataset(dataset_id_or_alias)

        dataset = Dataset.from_dict(dataset_json)
        data = catalog.get_data(dataset.dataset_id, data_format)

        if data_format in (DataFormat.RAW, DataFormat.CSV):
            return data

        if not data:
            return None

        data = json.loads(data)

        if data_format is DataFormat.CHARTJS:
            return chartjs.to_chart(dataset, data)

        # reassemble data with metadata labels
        if dataset.metadata:
            metadata = ChartJSMetadata.from_str(dataset.metadata)

            data_point: dict
            for i, data_point in enumerate(data):
                data[i] = {metadata.get_label(k) if metadata.get_label(
                    k) else k: v for k, v in data_point.items()}

        return data

    def get_dataset(self, dataset_id_or_alias: str, raw: bool = False) -> Dataset:
        """
        Gets a dataset

        Args:
            dataset_id_or_alias(str): Dataset ID or alias
            raw(bool, optional): Whether to return the dataset as a raw string or not
            (defaults to False)

        Returns:
            Dataset: Dataset object

        Examples:

        Fetch a dataset as a Dataset object
        ```py
        # create MatatikaClient object
        # create 'dataset_id_or_alias' variable

        dataset = client.get_dataset(dataset_id_or_alias)
        print(dataset)
        ```

        Fetch a dataset as a raw string
        ```py
        # create MatatikaClient object
        # create 'dataset_id_or_alias' variable

        dataset = client.get_dataset(dataset_id_or_alias, raw=True)
        print(dataset)
        ```
        """

        catalog = Catalog(self)

        if is_uuid4(dataset_id_or_alias):
            dataset_json = catalog.get_dataset(dataset_id_or_alias)

        else:
            if not self.workspace_id:
                raise MatatikaException(
                    "Workspace ID must be provided to get a dataset by an alias")

            dataset_json = catalog.get_workspace_dataset(dataset_id_or_alias)

        if raw:
            return json.dumps(dataset_json)

        return Dataset.from_dict(dataset_json)
