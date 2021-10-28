import webbrowser
import wsgiref.simple_server
import wsgiref.util
import logging
import json
import urllib.parse as urlparse

from authlib.integrations.requests_client import OAuth2Session

_LOGGER = logging.getLogger(__name__)


class Flow(object):
    """
    """
    AUTHORIZATION_URL='https://oauth2.sky.blackbaud.com/authorization'


    def __init__(
        self,
        client,
        host,
        port
        ):
        """
        """
        self.client = client
        self.host = host
        self.port = port
        
        
    @classmethod
    def load_credentials(cls, sky_credentials):
        """Creates a :class:`Flow` instance from a sky_credentials file.

        Args:
            sky_credentials (str): The path to the sky credentials .json file.
            kwargs: Any additional parameters passed to
                :class:`authlib.integrations.requests_client.OAuth2Session`

        Returns:
            Flow: The constructed Flow instance.
        """
        with open(sky_credentials, "r") as json_file:
            credentials = json.load(json_file)

        # Parsing the url for the host and port
        url = urlparse.urlparse("http://localhost:8080")
        host = url.hostname
        port = url.port

        client = OAuth2Session(
            client_id = credentials['client_id'],
            client_secret = credentials['client_secret'],
            redirect_uri = credentials['redirect_uri'],
            token_endpoint='https://oauth2.sky.blackbaud.com/token',
            authorization_endpoint='https://oauth2.sky.blackbaud.com/authorization',
            token_endpoint_auth_method='client_secret_basic'
        )
        
        return cls(
            client,
            host,
            port
        )
    

    def run_local_server(
        self,
        open_browser=True
        ):
        """
        
        """
        wsgi_app = _RedirectWSGIApp("You may close the browser now")
        local_server = wsgiref.simple_server.make_server(
            "localhost", 8080, wsgi_app, handler_class=_WSGIRequestHandler
        )

        url, _ = self.authorization_url()

        if open_browser:
            webbrowser.open(url, new=1, autoraise=True)

        local_server.handle_request()

        # OAuth 2.0 should only occur over https.
        authorization_response = wsgi_app.last_request_uri.replace("http", "https")
        token = self.fetch_token(authorization_response=authorization_response)
        return token


    @property
    def redirect_uri(self):
        """The OAuth 2.0 redirect URI. Pass-through to
        ``self.oauth2session.redirect_uri``."""
        return self.oauth2session.redirect_uri
    

    def authorization_url(self) :
        """
        """
        return self.client.create_authorization_url(self.AUTHORIZATION_URL)


    def fetch_token(self, **kwargs):
        """
        """
        kwargs.setdefault("client_secret", self.client.client_secret)
        return self.client.fetch_token(self.client.metadata['token_endpoint'], **kwargs)
    
    
class _WSGIRequestHandler(wsgiref.simple_server.WSGIRequestHandler):
    """Custom WSGIRequestHandler.

    Uses a named logger instead of printing to stderr.
    """

    def log_message(self, format, *args):
        # pylint: disable=redefined-builtin
        # (format is the argument name defined in the superclass.)
        _LOGGER.info(format, *args)


class _RedirectWSGIApp(object):
    """WSGI app to handle the authorization redirect.

    Stores the request URI and displays the given success message.
    """
    def __init__(self, success_message):
        """
        Args:
            success_message (str): The message to display in the web browser
                the authorization flow is complete.
        """
        self.last_request_uri = None
        self._success_message = success_message

    def __call__(self, environ, start_response):
        """WSGI Callable.

        Args:
            environ (Mapping[str, Any]): The WSGI environment.
            start_response (Callable[str, list]): The WSGI start_response
                callable.

        Returns:
            Iterable[bytes]: The response body.
        """
        start_response("200 OK", [("Content-type", "text/plain")])
        self.last_request_uri = wsgiref.util.request_uri(environ)
        return [self._success_message.encode("utf-8")]

