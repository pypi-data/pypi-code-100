from typing import List
from provider import Provider
import requests
import json
import os
from loguru import logger


def pagination(url: str, token: str) -> List:
    headers = {
        'Authorization': f"Token {token}",
        'Content-Type': 'application/json'
    }
    results = []
    next_page = url
    while next_page:
        r = requests.get(next_page, headers=headers)
        response = json.loads(r.text)
        next_page = response['next']
        results.extend(response['results'])
    return results


class Connection:
    def __init__(self, stack, connection_type_id, connection_id, connection_name):
        self.stack = stack
        self.connection_type_id = connection_type_id
        self.connection_id = connection_id
        self.connection_name = connection_name


class ConnectionFactory:
    def __init__(self, provider):
        self.provider = provider

    def get_connection_types(self):
        """Retrieve all white-listed Connection types on any particular stack.

        The result is paginated

        https://help.adverity.com/hc/en-us/articles/360011404100-Connections-Connection-Types
        curl -X GET https://ENDPOINT/api/connection-types/ -H "Authorization: Token TOKEN_VALUE" 
        """
        try:
            results = pagination(f"https://{self.provider.endpoint}/api/connection-types/", self.provider.get_token())
        except:
            logger.exception("Failed to get connection types")
        return results

    def retrieve_connections(self, connection_type_id: str):
        """Use the Connection type ID, e.g. 123 to retrieve all connections of this type.

        curl -H https://ENDPOINT/api/connection-types/123/connections/ -H "Authorization: Token TOKEN_VALUE"

        :param connection_type_id: connection type id
        :type connection_type_id: str
        """
        try:
            results = pagination(
                f"https://{self.provider.endpoint}/api/connection-types/{connection_type_id}/connections/", self.provider.get_token())
        except:
            logger.exception(f"Failed to retrieve connections of type {connection_type_id}")
        return results

    def create_connection(self, connection_type_id: str, stack_id: int, name: str, **args) -> Connection:
        """Create Connection

        make an OPTIONS request against the Connection type of your choice to find out about available/mandatory options
        curl -X OPTIONS https://YOUR_STACK.datatap.adverity.com/api/connection-types/123/connections/ -H 'Authorization: Token TOKEN_VALUE'

        curl -X POST \
        https://YOUR_STACK.datatap.adverity.com/api/connection-types/123/connections/ \
        -H 'Authorization: Token TOKEN_VALUE' \
        -H 'Content-Type: application/json' \
        -d '{
        "datatype": "DATATYPE",
        "cron_type": "CRON_TYPE",
        "name": "NAME_OF_STREAM",
        "stack": WORKSPACE_ID
        }'
        """
        try:
            headers = {
                'Authorization': f"Token {self.provider.get_token()}",
                'Content-Type': 'application/json'
            }
            url = f"https://{self.provider.stack}.datatap.adverity.com/api/connection-types/{connection_type_id}/connections/"
            if connection_type_id == '739':
                # create connection for type 739, Facebook Ads Connection
                # name, required
                # no_validate, optional
                # stack, optional
                data = {
                    'name': name,
                    'stack': stack_id
                }
                response = requests.post(url, json=data, headers=headers)
                logger.info(response.text)
            else:
                raise Exception(f"Connection type {connection_type_id} is not implemented")
        except:
            logger.exception(f"Failed to create connection for connection_type_id {connection_type_id}")
            raise
        else:
            # check if the connection is already created or not
            try:
                return Connection(1, connection_type_id, json.loads(response.text)['id'], json.loads(response.text)['name'])
            except:
                logger.exception(f"This connection name already exists")
                raise Exception(f"This connection name already exists")

    def update_connection_token(self, connection: Connection, new_token: str):
        """Update token of the connection

        curl -X PATCH \
        https://ENDPOINT/api/connection-types/CONNECTION_TYPE_ID/connections/CONNECTION_ID/token/
        -H "Authorization: Token TOKEN_VALUE" \
        -H 'Content-Type: application/json' \
        -d access_token=SYSTEM_GENERATED_TOKEN \

        :param connection: adverity connection
        :type connection: Connection
        :param new_token: new connection token
        :type new_token: str
        """
        try:
            headers = {
                'Authorization': f"Token {self.provider.get_token()}",
                'Content-Type': 'application/json'
            }
            connection_id = connection.connection_id
            connection_type_id = connection.connection_type_id
            response = requests.patch(
                f"https://{self.provider.endpoint}/api/connection-types/{connection_type_id}/connections/{connection_id}/token/",
                headers=headers,
                json={'access_token': new_token, 'expires': '2100-01-01T01:01'}
            )
            logger.info(response.text)
        except:
            logger.exception(f"Failed to update token on connection type {connection_type_id} id {connection_id}")


if __name__ == '__main__':
    username = os.getenv('adverity_username')
    password = os.getenv('adverity_password')

    # stack_id 1
    stack = 'rubix'
    p = Provider(stack=stack, username=username, password=password)

    # create connection factory
    connection_factory = ConnectionFactory(provider=p)

    # get all connection types
    results = connection_factory.get_connection_types()
    for result in results:
        if result['id'] == 739:
            print(result)

    # get all connections for a certain connection type
    results = connection_factory.retrieve_connections('739')
    print(results)

    # create connection
    # try:
    #     connection_factory.create_connection('739', 1,  'act_319883982')
    # except:
    #     pass

    # # update connection token
    # test_connection = Connection(1, '739', 21, 'test1')
    # new_token = 'EAAhMVyE1D1kBAOVnBJadfloQJiuVZAzfzHE4jnYfMbKYNBrH1Iu3OZBXWfXsIZAtI1fVZAYCwqyOoxQpDKkcW0jdULTZAyGbH3fu5oUaMs7i6PXoo0yEiEo9G3e1QaRTEDCZBrLkxMqpC7tFmXE364M1jzV4KgwOKQWpOqcb4YCNaacwhJxs9a'
    # connection_factory.update_connection_token(test_connection, new_token)
