import requests


def _delete_from_onedrive(token, site_id, item_path):
    delete_request_headers = {
        "Authorization": f"Bearer {token}",
    }

    meta_link = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root:/{item_path}"

    resp = requests.delete(meta_link, headers=delete_request_headers)
    resp.raise_for_status()
    print(f"File {item_path} has been successfully removed from OneDrive")


def delete_from_onedrive(token, site_id, item_path):
    return _delete_from_onedrive(token, site_id, item_path)
