import requests
import os
from .shared import (try_from_response, SITE_ID, CLIENT_ID, TENANT_ID, auth_token,
                     response_content_to_dict, download_file)


def _obtain_download_link(token, site_id, item_path):
    """Gets a direct download link to an item in OneDrive.

    Args:
        `token` (:obj:`str`): OAuth2 token as returned by `auth_token` function
        `site_id` (:obj:`str`): Site ID, unique identifier of the Sharepoint site
            under which a OneDrive instance is hosted. Can be extracted by looking
            at the source code of the webpage in the browser. Just make sure
            you don't confuse your Personal SiteId (your OneDrive instance)
            with the site that serves actual shared resources.
        `item_path` (:obj:`str`): Path relative to the root of OneDrive.

    Returns:
        Name and Direct download link (:obj:`tuple` of :obj:`str`, :obj:`str`).
    """

    download_request_headers = {
        "Authorization": f"Bearer {token}",
        # "Host": "technica-engineering.de"  # this seems to be the wrong hostname... too bad!
    }

    # download_link = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{item_id}/content"  # noqa: E501
    meta_link = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:/{item_path}"
    # meta_link = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root"
    # download_link = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:/{item_path}/content"  # noqa: E501

    resp = requests.get(meta_link, headers=download_request_headers)
    resp = response_content_to_dict(resp)

    download_link = None
    name = None

    name = try_from_response(resp, "name", "Cannot obtain filename from MS Graph API response.")

    download_link = try_from_response(resp, "@microsoft.graph.downloadUrl",
                                      "Failed to obtain direct download link from MS Graph API")

    return name, download_link


def _download_from_onedrive(token, site_id, item_path, target_path=None):
    """Downloads a file from OneDrive

    Args:
        `token` (:obj:`str`): OAuth2 token as returned by `auth_token` function
        `site_id` (:obj:`str`): Site ID, unique identifier of the Sharepoint site
            under which a OneDrive instance is hosted. Can be extracted by looking
            at the source code of the webpage in the browser. Just make sure
            you don't confuse your Personal SiteId (your OneDrive instance)
            with the site that serves actual shared resources.
        `item_path` (:obj:`str`): Path relative to the root of OneDrive.
        `target_path` (:obj:`str`): Path to a folder where a specific
            file you're downloading shall be saved. If `None` (by default),
            the file will be saved to **current working directory**.

    Returns:
        Output file path (:obj:`str`)
    """

    name, download_link = _obtain_download_link(token, site_id, item_path)

    if target_path is None:
        output_path = name
    else:
        output_path = os.path.join(target_path, name)

    outpath = download_file(output_path, download_link)
    print(f"File download succeded, can be found here: {outpath}")
    return outpath


def is_cached(target_file_name, target_file_directory):
    """Checks whether a file exists in a given directory
    (whether it's cached).

    Args:
        `target_file_name` (:obj:`str`): filename to search for
        `target_file_directory` (:obj:`str`): path to the directory
            where to search for a given file

    Returns:
        :obj:`bool`, `True` if the file has been found,
        `False` otherwise
    """
    if not os.path.exists(target_file_directory):
        return False
    for f in os.listdir(target_file_directory):
        if f == target_file_name:
            return True
    else:
        return False


def download_from_onedrive(item_path, target_path=None, check_cache_first=True):
    """Downloads an item from OneDrive to a specified path
    or current working directory with pre-set connection
    to OneDrive (where Client ID, Tenant ID and Site ID)
    are set in the Environment variables.

    Args:
        `item_path` (:obj:`str`): Path relative to the root of OneDrive.
        `target_path` (:obj:`str`): Path to a folder where a specific
            file you're downloading shall be saved. If `None` (by default),
            the file will be saved to **current working directory**.
        `check_cache_first` (:obj:`str`): If `True` (default), before
            downloading anything from OneDrive the target path will
            be checked whether the file of the same name already exists.
            If that's the case this function will short circuit, printing
            out the information that the file is already there and doesn't
            need to be downloaded again.

    Returns:
        Output file path (:obj:`str`).
    """

    if check_cache_first:
        name = os.path.split(item_path)[-1]
        if is_cached(name, target_path):
            full_target_path = os.path.join(target_path, name)
            print(f"{full_target_path} says: I'm here! No need to download me again!")
            return full_target_path

    return _download_from_onedrive(
        auth_token(CLIENT_ID, TENANT_ID), SITE_ID, item_path, target_path)
