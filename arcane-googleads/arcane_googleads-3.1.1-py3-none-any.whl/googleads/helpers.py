from typing import Dict, Optional
from yaml import load, FullLoader

from arcane.datastore import Client as DatastoreClient
from arcane.core import UserRightsEnum, RightsLevelEnum, BadRequestError, BaseAccount, GOOGLE_ADS_USER_CREDENTIAL_KIND
from arcane.requests import call_get_route


def make_request_account_id(account_id: str) -> str:
    """ Removes '-' from account_id to make it valid for requests """
    return account_id.replace('-', '')


def get_google_ads_account(
    base_account: BaseAccount,
    clients_service_url: str,
    firebase_api_key: str,
    gcp_credentials_path: str,
    auth_enabled: bool = True
) -> Dict:
    url = f"{clients_service_url}/api/google-ads-account?account_id={base_account['id']}&client_id={base_account['client_id']}"
    accounts = call_get_route(
        url,
        firebase_api_key,
        claims={'features_rights':{UserRightsEnum.AMS_GTP: RightsLevelEnum.VIEWER}, 'authorized_clients': ['all']},
        auth_enabled=auth_enabled,
        credentials_path=gcp_credentials_path
    )
    if len(accounts) == 0:
        raise ValueError(f'Error while getting google ads account with: {base_account}. No account corresponding.')
    elif len(accounts) > 1:
        raise ValueError(f'Error while getting google ads account with: {base_account}. Several account corresponding: {accounts}')

    return accounts[0]


def _get_google_ads_user_crendential(
    user_email: str,
    datastore_client: Optional[DatastoreClient] = None,
    gcp_credentials_path: Optional[str] = None,
    gcp_project: Optional[str] = None
) -> Dict:
    if not datastore_client:
        if not gcp_credentials_path and not gcp_project:
            raise BadRequestError('gcp_credentials_path or gcp_project should not be None if datastore_client is not provided')
        datastore_client = DatastoreClient.from_service_account_json(
            gcp_credentials_path, project=gcp_project)
    query = datastore_client.query(kind=GOOGLE_ADS_USER_CREDENTIAL_KIND).add_filter('email', '=', user_email)
    users_credential = list(query.fetch())
    if len(users_credential) == 0:
        raise ValueError(f'Error while getting google ads user credentials with mail: {user_email}. No entity corresponding.')
    elif len(users_credential) > 1:
        raise ValueError(f'Error while getting google ads user credentials with mail: {user_email}. Several entities corresponding: {users_credential}')
    return users_credential[0]


def _get_login_customer_id_and_developer_token(mcc_credentials_path: str):
    ads_credentials_file = open(mcc_credentials_path)
    parsed_credentials_file = load(ads_credentials_file, Loader=FullLoader)

    return str(parsed_credentials_file["login_customer_id"]), parsed_credentials_file["developer_token"]

