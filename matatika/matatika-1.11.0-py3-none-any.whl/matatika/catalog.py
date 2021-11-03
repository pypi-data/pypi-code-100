"""catalog module"""

import requests
from requests.models import Response
from matatika.auth import get_access_token
from matatika.context import MatatikaContext
from matatika.exceptions import (
    DatasetNotFoundError,
    MatatikaException,
    NoDefaultContextSetError,
    WorkspaceNotFoundError,
    ChannelExistsError
)
from matatika.types import DataFormat
from matatika.dataset import Dataset
from matatika.channel import Channel


# pylint: disable=too-many-instance-attributes
class Catalog:
    """Class to handle client-side HTTP requests to the Matatika API"""

    def _refresh_access_token(self, response: Response, *_args, **_kwargs):
        """Try refreshing access token if `401 Unauthorized` received"""

        if not (self.client.client_id and self.client.client_secret) or response.status_code != 401:
            return None

        self.client.auth_token = get_access_token(self.client.client_id,
                                                  self.client.client_secret,
                                                  self.client.endpoint_url)
        if self.client._from_cli:  # pylint: disable=protected-access
            variables = {'auth_token': self.client.auth_token}
            try:
                MatatikaContext().update_default_context_variables(variables)
            except NoDefaultContextSetError:
                pass

        self.session.headers['Authorization'] = f'Bearer {self.client.auth_token}'
        response.request.headers.update(self.session.headers)
        response.request.deregister_hook(
            'response', self._refresh_access_token)

        return self.session.send(response.request)

    def __init__(self, client):

        self.client = client

        if not client.auth_token and (client.client_id and client.client_secret):
            client.auth_token = get_access_token(client.client_id,
                                                 client.client_secret,
                                                 client.endpoint_url)

        self.profiles_url = client.endpoint_url + '/profiles'
        self.workspaces_url = client.endpoint_url + '/workspaces'
        self.datasets_url = client.endpoint_url + '/datasets'
        self.workspace_channels_url = f'{self.workspaces_url}/{client.workspace_id}/channels/'
        self.workspace_datasets_url = f'{self.workspaces_url}/{client.workspace_id}/datasets'

        self.session = requests.Session()
        self.session.headers = {'Authorization': f'Bearer {client.auth_token}',
                                'content-type': 'application/json'}
        self.session.hooks['response'] = [self._refresh_access_token]

    def post_resources(self, resources):
        """Publishes a converted yaml file into a workspace"""

        if not self.client.workspace_id:
            raise MatatikaException("No workspace is set on the client")

        publish_responses = []

        for resource in resources:
            if isinstance(resource, Dataset):
                response = self.session.post(self.workspace_datasets_url,
                                            data=resource.to_json_str())
            elif isinstance(resource, Channel):
                response = self.session.put(self.workspace_channels_url + resource.name,
                                            data=resource.to_json_str())

                if response.status_code == 409:
                    raise ChannelExistsError(f"A channel with the name {resource.name} " +
                                            "already exists in your workspace.")

            if response.status_code == 400:
                raise MatatikaException(f"An error occurred while publishing supplied file: "
                                        f"{response.json()['message']}")

            if response.status_code == 404:
                raise WorkspaceNotFoundError(
                    self.client.workspace_id, self.client.workspace_id)

            response.raise_for_status()

            publish_responses.append(response)

        return publish_responses

    def get_workspaces(self):
        """Returns all workspaces the user profile is a member of"""

        response = self.session.get(self.workspaces_url)
        response.raise_for_status()

        json_data = response.json()
        workspaces = {}

        if json_data['page']['totalElements'] > 0:
            workspaces = json_data['_embedded']['workspaces']

        return workspaces

    def get_datasets(self):
        """Returns all datasets in the supplied workspace"""

        if not self.client.workspace_id:
            raise MatatikaException("No workspace is set on the client")

        response = self.session.get(self.workspace_datasets_url)
        response.raise_for_status()

        json_data = response.json()
        datasets = {}

        if json_data['page']['totalElements'] > 0:
            datasets = json_data['_embedded']['datasets']

        return datasets

    def get_channels(self):
        """Returns all channels in the supplied workspace"""

        if not self.client.workspace_id:
            raise MatatikaException("No workspace is set on the client")

        response = self.session.get(self.workspace_channels_url)
        response.raise_for_status()

        json_data = response.json()
        datasets = {}

        if json_data['page']['totalElements'] > 0:
            datasets = json_data['_embedded']['channels']

        return datasets

    def get_profile(self):
        """Returns the user profile"""

        response = self.session.get(self.profiles_url)
        response.raise_for_status()

        return response.json()['_embedded']['profiles'][0]

    def get_data(self, id_, data_format: DataFormat):
        """Returns the data from a dataset"""

        if data_format is DataFormat.CSV:
            self.session.headers['Accept'] = 'text/csv'

        response = self.session.get(f'{self.datasets_url}/{id_}/data')

        if response.status_code == 404:
            raise DatasetNotFoundError(id_, self.client.endpoint_url)

        response.raise_for_status()

        return response.text

    def get_dataset(self, id_):
        """Returns a dataset"""

        response = self.session.get(f'{self.datasets_url}/{id_}')

        if response.status_code == 404:
            raise DatasetNotFoundError(id_, self.client.endpoint_url)

        response.raise_for_status()

        return response.json()

    def get_workspace_dataset(self, id_or_alias):
        """Returns a workspace dataset"""

        if not self.client.workspace_id:
            raise MatatikaException("No workspace is set on the client")

        response = self.session.get(
            self.workspace_datasets_url + f'/{id_or_alias}')

        if response.status_code == 404:
            raise DatasetNotFoundError(
                id_or_alias, self.client.endpoint_url)

        response.raise_for_status()

        return response.json()

    def delete_dataset(self, id_):
        """Deletes a dataset"""

        response = self.session.delete(f'{self.datasets_url}/{id_}')

        if response.status_code == 404:
            raise DatasetNotFoundError(id_, self.client.endpoint_url)

        response.raise_for_status()

    def delete_workspace(self, id_):
        """Deletes a workspace"""

        response = self.session.delete(f'{self.workspaces_url}/{id_}')

        if response.status_code == 404:
            raise WorkspaceNotFoundError(id_, self.client.endpoint_url)

        response.raise_for_status()
