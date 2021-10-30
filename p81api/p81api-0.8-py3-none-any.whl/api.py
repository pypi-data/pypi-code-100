import http.client
import requests
import json
import urllib.request
from copy import copy
from dataclasses import asdict
from typing import List, Dict, Union

from dacite import from_dict

from .model import (
    Group,
    Err,
    Auth,
    CreateGroupResponse,
    User,
    CreateUserResponse,
    CreateGroupApiCallResult,
    CreateUserApiCallResult,
    ApiCallResultBase,
    ListUsersArguments,
    ListNetworksApiCallResult,
    Network,
    NetworkHealth,
    NetworkStatus,
    GetNetworksHealthApiCallResult
)

"""
P81 API
"""
_AUTH_URL = 'https://api.perimeter81.com/api/v1/auth/authorize'
_BASE_URL = 'https://api.perimeter81.com/api/rest'
_AUTH_HEADERS = {'Accept': 'application/json', 'Content-Type': 'application/json',
                 'Authorization': '<REPLACE_ME>'}


def authenticate(api_key: str) -> Auth:
    """
    Authenticate
    """

    def _make_headers(token: str) -> Auth:
        result: Dict = copy(_AUTH_HEADERS)
        result['Authorization'] = f'Bearer {token}'
        return result

    data: Dict = {'grantType': 'api_key', 'apiKey': api_key}
    headers: Dict = {'Content-type': 'application/json', 'accept': 'application/json'}
    auth: Dict = _post(_AUTH_URL, headers, data)
    return _make_headers(auth['data']['accessToken'])


def create_user(auth: Auth, user: User) -> CreateUserApiCallResult:
    """
    Create a User
    """
    return create_users(auth, [user])


def create_users(auth: Auth, users: List[User]) -> CreateUserApiCallResult:
    """
    Create a few Users
    """
    url: str = f'{_BASE_URL}/v1/users'
    errors: List[Err] = []
    results: List[CreateUserResponse] = []
    for user in users:
        payload = asdict(user)
        try:
            response: Dict = _post(url, auth, payload, [201])
            results.append(CreateUserResponse(**response))
        except Exception as e:
            errors.append(str(e))
    return CreateUserApiCallResult(len(errors) == 0, errors, results)


def delete_user(auth: Auth, user_id: str) -> ApiCallResultBase:
    """
    Delete a User
    """
    return delete_users(auth, [user_id])


def delete_users(auth: Auth, user_ids: List[str]) -> ApiCallResultBase:
    """
    Delete a few Users
    """
    return _do_delete(auth, user_ids, '{}/v1/users/{}')


def _list_users(auth: Auth, list_users_args: ListUsersArguments):
    # TODO: implement
    # see https://perimeter81.slack.com/archives/D02HSK04B8B/p1634457043001200
    pass


def get_network_health(auth: Auth, network_id: str) -> GetNetworksHealthApiCallResult:
    """
    Get Network health
    """
    return get_networks_health(auth, [network_id])


def get_networks_health(auth: Auth, network_ids: List[str]) -> GetNetworksHealthApiCallResult:
    """
    Get a few Networks health
    """
    url_template: str = '{}/v1/networks/{}/health'
    errors: List[Err] = []
    results: List[NetworkHealth] = list()
    for _id in network_ids:
        url: str = url_template.format(_BASE_URL, _id)
        try:
            temp_result: Dict = _get(url, auth)
            results.append([from_dict(NetworkStatus, x) for x in temp_result['data']])
        except Exception as e:
            errors.append(str(e))
    return GetNetworksHealthApiCallResult(len(errors) == 0, errors, results)


def list_networks(auth: Auth) -> ListNetworksApiCallResult:
    """
    List Networks
    """
    url: str = f'{_BASE_URL}/v1/networks'
    try:
        temp_results: List[Dict] = _get(url, auth)
        results: List[Network] = [from_dict(Network, x) for x in temp_results['data']]
        return ListNetworksApiCallResult(True, None, results)
    except Exception as e:
        return ListNetworksApiCallResult(False, [str(e)], None)


def create_group(auth: Auth, group: Group) -> CreateGroupApiCallResult:
    """
    Create a Group
    """
    return create_groups(auth, [group])


def create_groups(auth: Auth, groups: List[Group]) -> CreateGroupApiCallResult:
    """
    Create a few Groups
    """

    url: str = f'{_BASE_URL}/v1/groups'
    errors: List[Err] = []
    results: List[Union[CreateGroupResponse, str]] = []
    for group in groups:
        payload = asdict(group)
        try:
            response: Dict = _post(url, auth, payload, [201, 409])
            results.append(CreateGroupResponse(**response))
        except Exception as e:
            errors.append(str(e))
    return CreateGroupApiCallResult(len(errors) == 0, errors, results)


def delete_group(auth: Auth, group_id: str) -> ApiCallResultBase:
    return delete_groups(auth, [group_id])


def delete_groups(auth: Auth, group_ids: List[str]) -> ApiCallResultBase:
    return _do_delete(auth, group_ids, '{}/v1/groups/{}')


def _do_delete(auth: Auth, ids: List[str], url_template: str) -> ApiCallResultBase:
    errors: List[Err] = []
    for _id in ids:
        url: str = url_template.format(_BASE_URL, _id)
        try:
            _delete(url, auth)
        except Exception as e:
            errors.append(str(e))
    return ApiCallResultBase(len(errors) == 0, errors)


def _get(url: str, headers: Dict, expected_status_codes: List[int] = [200]) -> List[Dict]:
    r = requests.get(url, headers=headers)
    if r.status_code not in expected_status_codes:
        raise Exception(
            f'Expected status code: {expected_status_codes}. Actual status code: {r.status_code}. Reason: {r.text}')
    else:
        return r.json()


def _delete(url: str, headers: Dict, expected_status_codes: List[int] = [200]) -> None:
    r = requests.delete(url, headers=headers)
    if r.status_code not in expected_status_codes:
        raise Exception(
            f'Expected status code: {expected_status_codes}. Actual status code: {r.status_code}. Reason: {r.text}')


def _post(url: str, headers: Dict, payload: Dict, expected_status_codes: List[int] = [200]) -> Dict:
    r = requests.post(url, headers=headers, data=json.dumps(payload))
    if r.status_code not in expected_status_codes:
        response_data = r.json()
        msg = response_data.get('message')
        # REST API bug (P81-5506) - 409 should be returned - however 400 is returned.
        # so we look at the message to see it we have a duplicate. Jira ticket was opened
        if msg.startswith('DUPLICATE_'):
            return {'duplicate': True}
        raise Exception(
            f'Expected status code: {expected_status_codes}. Actual status code: {r.status_code}. Reason: {r.text}')
    else:
        return r.json()
