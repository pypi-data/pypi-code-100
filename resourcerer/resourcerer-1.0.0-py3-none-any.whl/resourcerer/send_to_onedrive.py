import requests
from .shared import (try_from_response, SITE_ID, CLIENT_ID,
                     TENANT_ID, auth_token, response_content_to_dict, upload_file)

# "@odata.type" => "microsoft.graph.driveItemUploadableProperties",
#                         "@microsoft.graph.conflictBehavior" => "rename",
#                         "name" => $file_name


def _send_to_onedrive(token, site_id, item_path, target_path):
    upload_request_headers = {
        "Authorization": f"Bearer {token}"
    }
    upload_request_body = {
        "item": {
            "@microsoft.graph.conflictBehavior": "replace",
        }
    }
    upload_session_start_url = \
        f"https://graph.microsoft.com/v1.0/sites/{site_id}" + \
        f"/drive/root:/{item_path}:/createUploadSession"
    print(upload_session_start_url)
    resp = requests.post(upload_session_start_url,
                         headers=upload_request_headers, json=upload_request_body)
    upload_url = try_from_response(response_content_to_dict(
        resp), "uploadUrl", "Response did not contain upload URL. Failed to start upload session")
    upload_file(target_path, upload_url)
    print(f"Upload succesful. File located at: {item_path}")


def send_to_onedrive(item_path, target_path):
    return _send_to_onedrive(
        auth_token(CLIENT_ID, TENANT_ID), SITE_ID, item_path, target_path)
