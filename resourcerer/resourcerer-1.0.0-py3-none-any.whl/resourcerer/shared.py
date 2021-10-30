import os
import json
import requests
import warnings

SECRET = os.environ.get("MSGRAPH_API_KEY")
CLIENT_ID = os.environ.get("MSGRAPH_CLIENT_ID")
TENANT_ID = os.environ.get("MSGRAPH_TENANT_ID")
SITE_ID = os.environ.get("MSGRAPH_SITE_ID")


if not CLIENT_ID:
    CLIENT_ID = "08e33f13-a595-40d4-99f5-2ebefee0984d"
if not TENANT_ID:
    TENANT_ID = "1f04372a-6892-44e3-8f58-03845e1a70c1"
if not SITE_ID:
    SITE_ID = "5c7ce9f9-d466-437c-b0d1-ecf6e157f37b"


if not SECRET:
    # fall back on `keyring` when `MSGRAPH_KEY`
    # env var is not set
    import keyring
    SECRET = keyring.get_password("MSGraphApiKey", "system")
    if not SECRET:
        warnings.warn("CAUTION! Getting Secret from Credential Store Failed!")


def try_from_response(resp_dict, dict_key, error_msg):
    try:
        val = resp_dict[dict_key]
        return val
    except KeyError:
        print(resp_dict)
        raise KeyError(error_msg)


def response_content_to_dict(resp):
    return json.loads(str(resp.content, encoding='utf-8'))


def auth_token(client_id, tenant_id):
    """Gets MS Graph authentication token from
    OAuth2 authority server.

    Args:
        `client_id` (:obj:`str`): Client ID of the application
            (available in Azure Portal, where you registered
            your application).
        `tenant_id` (:obj:`str`): Tenant ID, unique identifier
            of MS Graph tenancy, can be found in Azure portal
            as well.

    Returns:
        Token string.
    """

    token_request_payload = {
        "client_id": client_id,
        "scope": "https://graph.microsoft.com/.default",
        "client_secret": SECRET,
        "grant_type": "client_credentials"
    }

    token_request_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"

    resp = requests.post(token_request_url, data=token_request_payload)
    resp = response_content_to_dict(resp)

    token = None

    token = try_from_response(resp, 'access_token',
                              "Failed to obtain access token from MS Graph OAuth endpoint.")
    return token


def download_file(name, url):
    # snatched from:
    # https://stackoverflow.com/questions/16694907/download-large-file-in-python-with-requests
    # NOTE the stream=True parameter below
    # NOTE if needed, MS Graph API supports Range header, e.g. `Range: bytes=0-1023`.
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        p = os.path.split(name)
        pre_path = os.path.join(*p[:-1])
        filename = p[-1]
        if not os.path.exists(pre_path):
            os.makedirs(pre_path)
        with open(os.path.join(pre_path, filename), 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)
    return name


def read_in_chunks(file_object, chunk_size=65536):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def upload_file(name, url):
    # adapted from: https://gist.github.com/nbari/7335384
    p = os.path.split(name)
    pre_path = os.path.join(*p[:-1])
    filename = p[-1]
    headers = {}
    index = 0
    content_size = os.stat(os.path.abspath(name)).st_size
    with open(os.path.join(pre_path, filename), 'rb') as f:
        for chunk in read_in_chunks(f, 327680):
            offset = index + len(chunk)
            headers['Content-Type'] = 'application/octet-stream'
            headers['Content-Length'] = str(content_size)
            headers['Content-Range'] = f'bytes {index}-{offset-1}/{content_size}'
            r = requests.put(url, data=chunk, headers=headers)
            # print(r.json())
            r.raise_for_status()
            print(f"Uploading {filename} bytes: {index}-{offset-1}, response: {r.status_code}")
            index = offset
    return name
