import os

from pymetrics_assessment_api_client import Client
from pymetrics_assessment_api_client.api.default import \
    mercury_get_config, mercury_o_auth
from pymetrics_assessment_api_client.examples.constants import BASE_URL, \
    ENV_NAME_X_API_KEY, ENV_NAME_CLIENT_ID, ENV_NAME_CLIENT_SECRET
from pymetrics_assessment_api_client.models import OAuthTokenRequest, \
    OAuthTokenResponse, MercuryConfiguration
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

    oauth_response: OAuthTokenResponse = auth_response.parsed
    x_api_key = os.getenv(ENV_NAME_X_API_KEY)
    auth = f"Bearer {oauth_response.access_token}"

    get_config_response: Response = mercury_get_config.sync_detailed(
        client=client,
        authorization=auth,
        x_api_key=x_api_key
    )
    parsed_get_config_response: MercuryConfiguration = get_config_response.parsed

    print(f"Successfully retrieved all assessments: {parsed_get_config_response.to_dict()}")


if __name__ == '__main__':
    main()

