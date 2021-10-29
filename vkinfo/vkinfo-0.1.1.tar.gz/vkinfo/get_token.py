import logging
import webbrowser
import argparse

def get_access_token(client_id: int, scope: str) -> None:
    """Get user access token. requires to log in
    and grant neccessary permisions to vkinfo app.

    Can be used as independant script via __main__, if
    explicit arguments given.

    This function opens auth Tab in webbrowser.
    After accepting permissions you'll be redirected to blank page,
    your access token is going to be inside url text like this:
    [https://oauth.vk.com/blank.html#access_token={your_token}&expires_in=*&user_id=*]
    Make sure to copy your token, otherwise you wont be able to run main script.

    Args:
        client_id: ID of an app, on whose behalf reqs are made
        scope: permissions needed for proper execution of an app
    """
    assert isinstance(client_id, int), 'clinet_id must be positive integer'
    assert isinstance(scope, str), 'scope must be string'
    assert client_id > 0, 'clinet_id must be positive integer'
    url = """\
    https://oauth.vk.com/authorize?client_id={client_id}&\
    redirect_uri=https://oauth.vk.com/blank.hmtl&\
    scope={scope}&\
    &response_type=token&\
    display=page\
    """.replace(" ", "").format(client_id=client_id, scope=scope)
    logging.info('Openning auth page in webbrowser..')
    webbrowser.open_new_tab(url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("client_id", help="Application Id", type=int)
    parser.add_argument("-s", dest="scope", help="Permissions", type=str, default="", required=False)
    args = parser.parse_args()
    get_access_token(args.client_id, args.scope)