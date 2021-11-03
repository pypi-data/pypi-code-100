""" Rally Authentication support for the Requests library.

Provides access for Decision Engine presets to Rally v2 API

Import example:

>>> from rally_token_auth import token_auth
"""
__all__ = ['RallyTokenAuth']


class RallyTokenAuth:
    """ Authentication class used with `Requests <https://docs.python-requests.org/en/latest/>`_
    python library

    :param token: Token to use for request authentication, defaults to current evaluate value
    :type token: str, optional

    Usage:

    >>> my_auth = RallyTokenAuth()

        **OR**

    >>> my_auth = RallyTokenAuth(token='my-token')    # Use your own token

    >>> resp = requests.get('https://demo.sdvi.com/api/v2/assets', auth=my_auth)
    >>> print(resp.json())
    {'data': [...], 'links': {...}, ...}
    """
    _app_id = 'rally-user-request'

    def __init__(self, token=None):
        self.token = token

        try:
            import rally

            job_uuid = rally.context.context(rally.context.JOB_UUID) or None
            self._app_id = f'evaluate-{job_uuid}' if job_uuid else self._app_id

            if not self.token:
                self.token = rally._session.context(rally.context.RALLY_API_TOKEN)
        except ImportError:
            # Do not blow up if SDK is unavailable
            # User-supplied token may still be valid
            pass

        if not self.token:
            raise ValueError('must supply a token if Rally module is unavailable')
        if not isinstance(self.token, str):
            raise ValueError('supplied token must be a string')

    def __call__(self, req, *args, **kwargs):
        req.headers.update({
            'X-SDVI-Client-Application': self._app_id,
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        })
        return req
