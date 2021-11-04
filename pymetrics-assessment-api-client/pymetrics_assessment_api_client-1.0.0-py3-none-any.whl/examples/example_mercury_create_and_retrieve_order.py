import os

from pymetrics_assessment_api_client import Client
from pymetrics_assessment_api_client.examples.constants import BASE_URL, \
    ENV_NAME_X_API_KEY, ENV_NAME_CLIENT_ID, ENV_NAME_CLIENT_SECRET, \
    ASSESSMENT_ID
from pymetrics_assessment_api_client.models import MercuryAssessmentOrder, \
    OAuthTokenRequest, OAuthTokenResponse, MercuryCandidate, \
    MercuryOrderRequest, MercuryAssessmentOrderMetadata, \
    MercuryOrderCreateResponse
from pymetrics_assessment_api_client.api.default import mercury_retrieve_order, \
    mercury_o_auth, mercury_create_order

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

    candidate = MercuryCandidate(
        email="test@example.com",
        first_name="Test",
        last_name="Example",
        external_id="test_example"
    )

    meta_data = MercuryAssessmentOrderMetadata()
    meta_data.additional_properties = {"job_name": "accountant"}

    order_request = MercuryOrderRequest(
        candidate=candidate,
        assessment_id=ASSESSMENT_ID,
        application_id="test_example_002",
        metadata=meta_data
    )

    create_order_response: Response = mercury_create_order.sync_detailed(
        client=client,
        json_body=order_request,
        x_api_key=x_api_key,
        authorization=auth
    )
    parsed_create_order_response: MercuryOrderCreateResponse = create_order_response.parsed

    order_uuid = parsed_create_order_response.order.id

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

