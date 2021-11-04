import os

from pymetrics_assessment_api_client import Client
from pymetrics_assessment_api_client.api.default import \
    mercury_retrieve_order, \
    mercury_o_auth
from pymetrics_assessment_api_client.examples.constants import BASE_URL, \
    ENV_NAME_X_API_KEY, ENV_NAME_CLIENT_ID, ENV_NAME_CLIENT_SECRET, ORDER_UUID
from pymetrics_assessment_api_client.models import MercuryAssessmentOrder, \
    OAuthTokenRequest, OAuthTokenResponse
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

    order_uuid = ORDER_UUID

    get_order_response: Response = mercury_retrieve_order.sync_detailed(
        client=client,
        uuid=order_uuid,
        authorization=auth,
        x_api_key=x_api_key,
        report=False
    )
    parsed_get_order_response: MercuryAssessmentOrder = get_order_response.parsed

    print(f"Successfully retrieved order: {parsed_get_order_response.to_dict()}")


if __name__ == '__main__':
    main()

