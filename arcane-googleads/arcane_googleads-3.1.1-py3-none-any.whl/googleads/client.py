from typing import Dict, Optional, cast
import backoff
import json

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.oauth2.credentials import Credentials

from arcane.core.exceptions import GOOGLE_EXCEPTIONS_TO_RETRY, BadRequestError
from arcane.core.types import BaseAccount
from arcane.datastore import Client as DatastoreClient
from arcane.secret import decrypt

from .exceptions import GoogleAdsAccountLostAccessException
from .helpers import get_google_ads_account, _get_google_ads_user_crendential, _get_login_customer_id_and_developer_token


_GOOGLE_ADS_VERSION = "v7"


def get_exception_message(account_id: str, access_token: Optional[str] = None) -> str:
    if access_token:
        return F"We cannot access your account with the id: {account_id}. Are you sure you have access and entered correct ID?"
    else:
        return F"We cannot access your account with the id: {account_id} from the Arcane Manager Account. Are you sure you granted access and gave the correct ID?"

# TODO: Delete access token, developer token and login_customer_id logic when AMCC is finished
def get_google_ads_client(
    mcc_credentials_path: Optional[str] = None,
    access_token: Optional[str] = None,
    login_customer_id: Optional[str] = None,
    developer_token: Optional[str] = None,
    google_ads_account: Optional[Dict] = None,
    base_account: Optional[BaseAccount] = None,
    clients_service_url: Optional[str] = None,
    firebase_api_key: Optional[str] = None,
    gcp_credentials_path: Optional[str] = None,
    auth_enabled: bool = True,
    datastore_client: Optional[DatastoreClient] = None,
    gcp_project: Optional[str] = None,
    secret_key_file: Optional[str] = None
) -> GoogleAdsClient:
    """Initialize google ads client depending on arguments furnished
    Priority order is: access_token > creator_email (obtained with google_ads_account/google_ads_account_id) > credentials_path
    Args:
        mcc_credentials_path (Optional[str], optional): mcc credentials. Defaults to None.
        access_token (Optional[str], optional): token obtained with client side oauth pattern. Defaults to None.
        login_customer_id (Optional[str], optional): additionnal info needed in client side oauth pattern. Defaults to None.
        developer_token (Optional[str], optional): developer token for accessing the API. Defaults to None.
        google_ads_account (Optional[Dict], optional): Account for which we want to init google ads client. Defaults to None.
        base_account (Optional[BaseAccount], optional): Account information needed to get the account for which we want to init google ads client. Defaults to None.
        clients_service_url: (Optional[str], optional): Needed for getting goolge ads account if not provided. Defaults to None.
        firebase_api_key: (Optional[str], optional): Needed for getting goolge ads account if not provided. Defaults to None.
        gcp_credentials_path: (Optional[str], optional): Needed for getting goolge ads account if not provided. Defaults to None.
        auth_enabled: (bool, optional): Needed for getting goolge ads account if not provided. Defaults to True.
        datastore_client: (Optional[str], optional): Needed for getting google_ads_user_credential. Defaults to None.
        gcp_project: (Optional[str], optional): Needed for getting google_ads_user_credential. Defaults to None.
        secret_key_file: (Optional[str], optional): Needed for decrypt google_ads_user_credential. Defaults to None.
    Raises:
        ValueError
        arcane.core.BadRequestError

    Returns:
        GoogleAdsClient: GoogleAdsClient
    """

    if access_token:
        credentials = Credentials(token=access_token, scopes='https://www.googleapis.com/auth/adwords')
        return GoogleAdsClient(
            credentials,
            developer_token,
            login_customer_id=login_customer_id
        )
    elif mcc_credentials_path and (google_ads_account or base_account):
        if google_ads_account is None and base_account is None:
            raise BadRequestError('google_ads_account and base_account should not be None simultaneously')
        if google_ads_account is None:
            if not clients_service_url or not firebase_api_key or not gcp_credentials_path:
                raise BadRequestError('clients_service_url or firebase_api_key or  gcp_credentials_path should not be None if google_ads_account is not provided')
            base_account = cast(BaseAccount, base_account)
            google_ads_account = get_google_ads_account(
                base_account,
                clients_service_url,
                firebase_api_key,
                gcp_credentials_path,
                auth_enabled
            )
        creator_email = google_ads_account.get('creator_email')
        if creator_email:
            login_customer_id, developer_token = _get_login_customer_id_and_developer_token(mcc_credentials_path)
            if not secret_key_file:
                raise BadRequestError('secret_key_file should not be None while using user access protocol')
            elif not developer_token:
                raise BadRequestError('developer_token should not be None while using user access protocol')
            user_credentials = _get_google_ads_user_crendential(creator_email, datastore_client, gcp_credentials_path, gcp_project)
            credentials = decrypt(user_credentials['credentials'], secret_key_file).decode('utf-8')
            credentials = Credentials(
                **json.loads(credentials)
            )
            return GoogleAdsClient(
                credentials,
                developer_token
            )
        return GoogleAdsClient.load_from_storage(mcc_credentials_path)
    # TODO: Clean this elif when updating check access acount in AMCC track
    elif mcc_credentials_path:
        return GoogleAdsClient.load_from_storage(mcc_credentials_path)
    else:
        raise ValueError('one of the following arguments must be specified: access_token or (mcc_credentials_path and (google_ads_account or google_ads_account_id))')


def get_google_ads_service(service_name: str, google_ads_client: GoogleAdsClient, version: str = _GOOGLE_ADS_VERSION):
    return google_ads_client.get_service(service_name, version=version)

@backoff.on_exception(backoff.expo, GOOGLE_EXCEPTIONS_TO_RETRY, max_tries=5)
def check_access_account(
    account_id: str,
    adscale_key: Optional[str] = None,
    access_token: Optional[str] = None,
    login_customer_id: Optional[str] = None,
    developer_token: Optional[str] = None
):
    """From an account id check if Arcane has access to it"""

    google_ads_client = get_google_ads_client(adscale_key, access_token, login_customer_id, developer_token)
    google_ads_service = get_google_ads_service('GoogleAdsService', google_ads_client)

    query = f"""
        SELECT
          customer_client.manager
        FROM customer_client
        WHERE customer_client.id = '{account_id}'"""
    search_query = google_ads_client.get_type(
        "SearchGoogleAdsRequest"
    )
    search_query.customer_id = account_id
    search_query.query = query
    try:
        response = list(google_ads_service.search(search_query))
        if len(response) == 0:
            raise GoogleAdsAccountLostAccessException(get_exception_message(account_id, access_token))
        response = response[0]
    except GoogleAdsException as err:
        if "USER_PERMISSION_DENIED" in str(err):
                raise GoogleAdsAccountLostAccessException(get_exception_message(account_id, access_token))
        elif "CUSTOMER_NOT_FOUND" in str(err):
            raise GoogleAdsAccountLostAccessException(f"We cannot find this account ({account_id}). Are you sure you entered the correct id?")
        else:
            raise GoogleAdsAccountLostAccessException(f"We cannot access this account ({account_id}). Are you sure you entered the correct id?")

    if response.customer_client.manager:
        raise GoogleAdsAccountLostAccessException('This account ID is a MCC. Please enter a Google Ads Account.')
