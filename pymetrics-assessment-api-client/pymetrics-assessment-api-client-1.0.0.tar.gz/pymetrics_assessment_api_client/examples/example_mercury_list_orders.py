import os

from pymetrics_assessment_api_client import Client
from pymetrics_assessment_api_client.api.default import mercury_list_orders, \
    mercury_o_auth
from pymetrics_assessment_api_client.examples.constants import BASE_URL, \
    ENV_NAME_X_API_KEY, ENV_NAME_CLIENT_ID, ENV_NAME_CLIENT_SECRET, \
    CANDIDATE_ID, JOB_APPLICATION_ID
from pymetrics_assessment_api_client.models import OAuthTokenRequest, \
    OAuthTokenResponse, MercuryListOrdersRequest, \
    MercuryListOrdersResponse
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

    list_orders_request_by_candidate_id = MercuryListOrdersRequest(
        candidate_id=CANDIDATE_ID
    )

    list_orders_response_cand: Response = mercury_list_orders.sync_detailed(
        client=client,
        json_body=list_orders_request_by_candidate_id,
        x_api_key=x_api_key,
        authorization=auth
    )
    parsed_list_orders_response_cand: MercuryListOrdersResponse = list_orders_response_cand.parsed

    print(f"Successfully listed order(s) by candidate id: {parsed_list_orders_response_cand.to_dict()}")


    list_orders_request_by_job_id = MercuryListOrdersRequest(
        job_application_id=JOB_APPLICATION_ID
    )

    list_orders_response_job: Response = mercury_list_orders.sync_detailed(
        client=client,
        json_body=list_orders_request_by_job_id,
        x_api_key=x_api_key,
        authorization=auth
    )
    parsed_list_orders_response_job: MercuryListOrdersResponse = \
        list_orders_response_job.parsed

    print(
        f"Successfully listed order(s) by job application id: "
        f"{parsed_list_orders_response_job.to_dict()}")




if __name__ == '__main__':
    main()

