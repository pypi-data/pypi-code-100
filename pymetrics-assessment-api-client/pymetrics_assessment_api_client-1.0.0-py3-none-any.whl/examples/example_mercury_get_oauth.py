import os

from pymetrics_assessment_api_client import Client
from pymetrics_assessment_api_client.examples.constants import BASE_URL, \
    ENV_NAME_CLIENT_ID, ENV_NAME_CLIENT_SECRET
from pymetrics_assessment_api_client.models import OAuthTokenRequest, \
    MercuryErrorResponse
from pymetrics_assessment_api_client.api.default import mercury_o_auth
from pymetrics_assessment_api_client.models import OAuthTokenResponse
from pymetrics_assessment_api_client.types import Response


def main():
    client_id = os.getenv(ENV_NAME_CLIENT_ID)
    client_secret = os.getenv(ENV_NAME_CLIENT_SECRET)
    client = Client(base_url=BASE_URL)
    request = OAuthTokenRequest(client_id=client_id,
                                client_secret=client_secret,
                                grant_type="client_credentials")
    auth_response: Response = mercury_o_auth.sync_detailed(client=client,
                                                           json_body=request)
    if isinstance(auth_response.parsed, OAuthTokenResponse):
        auth_token_response = auth_response.parsed
        print(f"Access Token: {auth_token_response.access_token}")
    elif isinstance(auth_response.parsed, MercuryErrorResponse):
        error_response = auth_response.parsed
        print(f"Exception getting OAuth Token: {error_response.message}")


if __name__ == '__main__':
    main()

