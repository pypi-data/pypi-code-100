"""auth module"""

from auth0.v3.authentication import GetToken


PRODUCTION = 'identity.matatika.com'
STAGING = 'identity-staging.matatika.com'


def get_access_token(client_id: str, client_secret: str, endpoint_url: str, **_kwargs):
    """Returns an access token using client credentials"""

    domain = PRODUCTION if 'catalog.matatika' in endpoint_url else STAGING
    response_body = GetToken(domain).client_credentials(
        client_id,
        client_secret,
        endpoint_url
    )

    return response_body['access_token']
