class Base:
    debug = False
    api_key = None
    server_url = None
    response_url = "/"
    project_key = None
    status_key = "status"
    response_type = "json"
    message_key = "message"
    save_body_response = False
    save_body_response_exception = False

    def is_valid():
        if Base.api_key == None:
            return False
        if Base.server_url == None:
            return False
        if Base.project_key == None:
            return False

        if len(Base.api_key) < 20:
            return False
        if "http" not in Base.server_url:
            return False

        return True


class Massage:
    not_found_massage = "Not Found"
    auth_massage = "Illegal access"
    block_massage = "your are block"
    permission_massage = "Access denied"
    upload_massage = "Error in upload file"
    date_massage = "Error in recorded dates"
    duplicate_massage = "Item already exists"
    validator_massage = "Fields are not complete"
    other_massage = "The server cannot respond at this time"


def init(api_key, project_key, server_url, debug=False, response_url=None, response_type='json', status_key='status', message_key='message', save_response=False, save_response_exception=False):
    if server_url[-1] == "/":
        server_url = server_url[:-1]
    Base.debug = debug
    Base.api_key = api_key
    Base.server_url = server_url
    Base.project_key = project_key
    Base.response_url = response_url
    Base.response_type = response_type
    Base.save_body_response = save_response
    Base.status_key = status_key.replace(" ", "_")
    Base.message_key = message_key.replace(" ", "_")
    Base.save_body_response_exception = save_response_exception


def exceptionMessage(
        auth_massage=None,
        date_massage=None,
        block_massage=None,
        other_massage=None,
        upload_massage=None,
        duplicate_massage=None,
        validator_massage=None,
        not_found_massage=None,
        permission_massage=None):
    if auth_massage:
        Massage.auth_massage = auth_massage
    if date_massage:
        Massage.date_massage = date_massage
    if block_massage:
        Massage.block_massage = block_massage
    if other_massage:
        Massage.other_massage = other_massage
    if upload_massage:
        Massage.upload_massage = upload_massage
    if duplicate_massage:
        Massage.duplicate_massage = duplicate_massage
    if validator_massage:
        Massage.validator_massage = validator_massage
    if not_found_massage:
        Massage.not_found_massage = not_found_massage
    if permission_massage:
        Massage.permission_massage = permission_massage
