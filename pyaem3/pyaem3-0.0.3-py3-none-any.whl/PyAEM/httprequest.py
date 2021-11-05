import io
from urllib.parse import urlencode

import certifi
import pycurl

from .handlers import unexpected as handle_unexpected


def request(method, url, params, handlers, **kwargs):
    """Sends HTTP request to a specified URL.
    Parameters will be appended to URL automatically on HTTP get method.
    Response code will then be used to determine which handler should process the response.
    When response code does not match any handler, an exception will be raised.
    :param method: HTTP method (post, delete, get)
    :type method: str
    :param url: URL to send HTTP request to
    :type url: str
    :param params: Request parameters key-value pairs, use array value to represent multi parameters with the same name
    :type params: dict
    :param handlers: Response handlers key-value pairs, keys are response http code, values are callback methods
    :type handlers: dict
    :returns:  PyAemResult -- Result of the request containing status, response http code and body, and request info
    :raises: PyAemException
    """
    curl = pycurl.Curl()
    buffer = io.BytesIO()

    if method == 'post':
        curl.setopt(curl.POST, 1)
        curl.setopt(curl.POSTFIELDS, urlencode(params, True))
    elif method == 'delete':
        curl.setopt(curl.CUSTOMREQUEST, method)
    elif method == 'head':
        curl.setopt(curl.HEADER, True)
        curl.setopt(curl.NOBODY, True)
    else:
        url = '{0}?{1}'.format(url, urlencode(params, True))

    curl.setopt(curl.URL, url)
    curl.setopt(curl.FOLLOWLOCATION, 1)
    curl.setopt(curl.FRESH_CONNECT, 1)
    curl.setopt(curl.WRITEDATA, buffer)
    curl.setopt(curl.CAINFO, certifi.where())

    try:
        curl.perform()

        response = {
            'http_code': curl.getinfo(pycurl.HTTP_CODE),
            'body': buffer.getvalue(),
            'request': {
                'method': method,
                'url': url,
                'params': params
            }
        }

        print(response['body'].decode('iso-8859-1'))

        if response['http_code'] in handlers:
            return handlers[response['http_code']](response)
        else:
            handle_unexpected(response)

    finally:
        curl.close()


def download_file(url, params, handlers, **kwargs):
    """Downloads a file from specified URL, the file will be downloaded to path specified in file kwarg.
    Parameters will be appended to URL automatically on HTTP get method.
    Response code will then be used to determine which handler should process the response.
    When response code does not match any handler, an exception will be raised.
    :param url: URL to send HTTP request to
    :type url: str
    :param params: Request parameters key-value pairs, use array value to represent multi parameters with the same name
    :type params: dict
    :param handlers: Response handlers key-value pairs, keys are response http code, values are callback methods
    :type handlers: dict
    :param kwargs: file (str) -- Location where the downloaded file will be saved to
    :type kwargs: dict
    :returns:  PyAemResult -- The result containing status, response http code and body, and request info
    :raises: PyAemException
    """
    curl = pycurl.Curl()
    url = '{0}?{1}'.format(url, urlencode(params, True))

    with open(kwargs['file'], 'wb') as f:
        curl.setopt(curl.URL, url)
        curl.setopt(curl.FOLLOWLOCATION, 1)
        curl.setopt(curl.FRESH_CONNECT, 1)
        curl.setopt(curl.WRITEDATA, f)
        curl.setopt(curl.CAINFO, certifi.where())

        curl.perform()

        response = {
            'http_code': curl.getinfo(pycurl.HTTP_CODE),
            'body': 'Download {0} to {1}'.format(url, kwargs['file']),
            'request': {
                'method': 'get',
                'url': url,
                'params': params
            }
        }

        curl.close()
        print(response['body'])

    if response['http_code'] in handlers:
        return handlers[response['http_code']](response, **kwargs)
    else:
        handle_unexpected(response)


def upload_file(url, params, handlers, **kwargs):
    """Uploads a file using the specified URL endpoint,
    the file to be uploaded must be available at the specified location in file kwarg.
    Parameters will be appended to URL automatically on HTTP get method.
    Response code will then be used to determine which handler should process the response.
    When response code does not match any handler, an exception will be raised.
    :param url: URL to send HTTP request to
    :type url: str
    :param params: Request parameters key-value pairs, use array value to represent multi parameters with the same name
    :type params: dict
    :param handlers: Response handlers key-value pairs, keys are response http code, values are callback methods
    :type handlers: dict
    :param kwargs: file (str) -- Location of the file to be uploaded
    :type kwargs: dict
    :returns:  PyAemResult -- The result containing status, response http code and body, and request info
    :raises: PyAemException
    """
    curl = pycurl.Curl()
    buffer = io.BytesIO()
    _params = []
    for key, value in params.items():
        _params.append((key, value))

    curl.setopt(curl.POST, 1)
    curl.setopt(curl.HTTPPOST, _params)
    curl.setopt(curl.URL, url)
    curl.setopt(curl.FOLLOWLOCATION, True)
    curl.setopt(curl.FRESH_CONNECT, 1)
    curl.setopt(curl.WRITEDATA, buffer)
    curl.setopt(curl.CAINFO, certifi.where())

    curl.perform()

    response = {
        'http_code': curl.getinfo(pycurl.HTTP_CODE),
        'body': buffer.getvalue(),
        'request': {
            'method': 'post',
            'url': url,
            'params': params
        }
    }

    # HTTP response code, e.g. 200.
    print('Status: %d' % curl.getinfo(curl.RESPONSE_CODE))
    # Elapsed time for the transfer.
    print('Time: %f' % curl.getinfo(curl.TOTAL_TIME))

    curl.close()

    if response['http_code'] in handlers:
        return handlers[response['http_code']](response, **kwargs)
    else:
        handle_unexpected(response)
