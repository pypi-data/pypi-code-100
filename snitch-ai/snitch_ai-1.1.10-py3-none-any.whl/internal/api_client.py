import json
import pkg_resources
from requests import Session
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager
from requests.packages.urllib3.util.retry import Retry
from urllib.parse import urljoin


# ignore hostname so long as the certificate matches the expected certificate since we do not know
# where the client is potentially hosting their LocalApi
class HostNameIgnoringAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       assert_hostname=False)


class ApiClient(Session):

    def __init__(self, *args, **kwargs):
        super(ApiClient, self).__init__(*args, **kwargs)
        self._retry_policy = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
        self._verify = pkg_resources.resource_filename("snitch_ai", "cert/snitch.localapi.crt")


    def request(self, method, url, *args, **kwargs):
        from snitch_ai import endpoint_address, cloud_endpoint, access_token

        # add access token
        if not access_token or len(access_token) == 0:
            raise Exception("You must set the snitch_ai.access_token variable to your access token before you can perform any API calls.")

        headers = {}
        if "headers" in kwargs:
            headers = kwargs["headers"]
            del kwargs["headers"]

        headers["Authorization"] = "Bearer " + access_token

        # set base URL
        base_url = endpoint_address
        if not base_url.endswith("/"):
           base_url += "/"

        url = urljoin(base_url, url)

        # handle cloud-hosted vs local-hosted endpoints
        if endpoint_address != cloud_endpoint:
            # verify self-signed certificate if using local endpoint but ignore hostname
            verify = self._verify
            self.mount("https://", HostNameIgnoringAdapter(max_retries=self._retry_policy))
        else:
            # default handling for cloud endpoint
            verify = True
            self.mount("https://", HTTPAdapter(max_retries=self._retry_policy))

        req = super(ApiClient, self).request(method, url, verify=verify, headers=headers, *args, **kwargs)

        # handle forbidden errors with additional information
        if req.status_code == 403 and req.text:
            default_message = "Request failed: Forbidden"

            try:
                content_type = req.headers.get("Content-Type")

                if content_type and "application/json" in content_type:
                        error = json.loads(req.text)
                        message = error["error"]["message"]

                        
                elif len(req.text) > 0:
                    message = req.text

                else:
                    message = default_message
            except:
                message = default_message
        
            raise Exception(message);

        # handle standard ASP.NET core auth error message
        if req.status_code == 401:
            auth_header = req.headers.get("WWW-Authenticate")
            if auth_header:
                parts = auth_header.split("error_description=")
                if len(parts) > 1:
                    raise Exception(f"Authentication failed: {parts[1]}")
            raise

        return req