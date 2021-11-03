from typing import Optional, Mapping
from identitylib.api_client import IdentityAPIClient


class NoSuchPhotoException(Exception):
    def __init__(self):
        super().__init__('No photo found for query criteria')


class PhotoClient (IdentityAPIClient):
    """
    A client which allows information to be fetched from the University Photo API.

    """

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        base_url: str = 'https://api.apps.cam.ac.uk/photo/v1beta1/',
        token_url: str = 'https://api.apps.cam.ac.uk/oauth/client_credential/accesstoken',
        config: Optional[Mapping] = {},
    ):

        super(PhotoClient, self).__init__(
            client_id, client_secret, base_url, token_url, config
        )

    def get_transient_image_url(self, photo_id: str):
        """
        Returns a transient image url which can be used to by unauthenticated clients
        to fetch the url of the given photo id.

        """
        response = self.session.get(
            f'{self.base_url}/photos/{photo_id}/content', allow_redirects=False
        )
        if response.status_code == 404:
            raise NoSuchPhotoException()
        response.raise_for_status()

        if not response.headers.get('Location'):
            raise RuntimeError('Photo API did not return a transient image url within redirect')

        return response.headers['Location']
