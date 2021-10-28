import requests
import logging
import json

from adara_privacy.utils import sdk_config
from adara_privacy.identity import Identity
from adara_privacy.streamers.streamer import Streamer


class AdaraPrivacyApiStreamer(Streamer):
    """
    Streams data to the Adara Privacy API.
    ** Requires a valid configuration to establish an authenticated connection to a provisioned client pipeline.
    """

    def __init__(self):
        super().__init__()

    def save(self, item: Identity, data=None):
        """
        Pushes an identity's token set to the Adara Privacy API.

        Args:
            item (Identity): An instance of an Identity that contains tokens to send
            to the Adara Privacy API.
            data: Optional arbitrary data to augment identity information
        """
        if isinstance(item, Identity):
            try:
                tokens = item.to_tokens()
                if data:
                    if isinstance(data, (str, bytes, bytearray)):
                        try:
                            data = json.loads(data)
                            tokens['data'] = data
                        except json.decoder.JSONDecodeError as errj:
                            logging.warning(
                                "Supplied arbitrary data cannot be decoded to JSON!"
                                " Data will not be added to the request. Error: {}".format(
                                    errj))
                    else:
                        tokens['data'] = data
                response = requests.post(
                    url=f'{sdk_config.privacy.audience_uri}/v2/send/{sdk_config.privacy.pipeline_id}',
                    headers={
                        'Content-Type': 'application/json',
                        'Authorization': "Bearer " + sdk_config.privacy.privacy_api_access_token,
                    },
                    data=json.dumps(tokens)
                )
                response.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                logging.error("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                logging.error("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                logging.error("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                logging.error("Other Request Error:", err)
        else:
            raise TypeError('Argument "item" must contain a reference to an instance of Identity.')
