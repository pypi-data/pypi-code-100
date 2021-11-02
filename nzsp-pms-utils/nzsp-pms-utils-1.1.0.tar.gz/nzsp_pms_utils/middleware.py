"""Contains NZSP PMS flask server middleware"""
import os
import requests
import flask
from flask.wrappers import Response

def verify_authorization() -> Response:
    """
    Verify authorization using Plant Managment system
    IAM Authorize API. if status 200 (OK), sets user identifier
    globally.

    Returns
    -------
    Response
        if status different than 200 (OK), reponse status.

    Raises
    ------
    KeyError
        When service_name is not set globally.

    Notes
    -----
    - Requires to set up the service name globally in
    an application before request.
    - Requires to set up environment vatiable IAM_AUTHORIZE_API.

    See Also
    --------
    - Check PMS IAM documentation to know more about this middleware.

    Examples
    --------
    Setting up application before request
    >>> @app.before_request
    ... def set_service_name_globally():
    ...    g.service_name = SERVICE_NAME
    Calling it in a blueprint
    >>> from nzsp_pms_utils.middleware import verify_authorization
    ... bp.before_request(verify_authorization)
    """
    if not flask.g.get("service_name"):
        raise KeyError(
            "service_name was not set globally," +
            "read the docs to get more info"
        )
    iam_authorize_response = requests.get(
        url = os.getenv("IAM_AUTHORIZE_API"),
        headers = {
            "authorization": flask.request.headers.get("authorization"),
            "service_name": flask.g.get("service_name"),
            "action_name": flask.request.method + flask.request.path
        }
    )
    if iam_authorize_response.status_code == 200:
        json_response = iam_authorize_response.json()
        flask.g.user_identifier = json_response["user_identifier"]
    else:
        return flask.Response(status = iam_authorize_response.status_code)
