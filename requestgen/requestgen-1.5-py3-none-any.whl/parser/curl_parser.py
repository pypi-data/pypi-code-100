from requestgen.parser.parser import Parser
from requestgen.beans.http_request import HttpRequest
import argparse
import shlex
import re
from http.cookies import SimpleCookie
import logging as log
import base64

log.basicConfig(format='%(asctime)s - %(message)s', level=log.DEBUG)


class CurlParser(Parser):

    def __init__(self, curl_command):
        curl_command = curl_command.strip()
        if not curl_command.startswith('curl '):
            raise ValueError("Is the command starting with 'curl'?")
        curl_command = re.sub(r'\s+\\\s+', ' ', curl_command, flags=re.DOTALL)
        super().__init__(curl_command)
        self.curl_command = curl_command

    def get_http_request(self, curl) -> HttpRequest:
        """
        :return:
        """
        # Parser ensures that url exist

        http_request = HttpRequest()

        if not curl.url.startswith('http'):
            curl.url = f'https://{curl.url}'
        http_request.url = curl.url

        if curl.headers:
            headers = {}
            cookies = {}
            for header in curl.headers or []:
                try:
                    key, val = header.split(':', 1)
                    key = key.strip()
                    val = val.lstrip()
                except:
                    raise ValueError('Missing ":" in header')
                if key in ['Cookie', 'cookie']:
                    for cookie_name, cookie_value in SimpleCookie(val).items():
                        cookies[cookie_name] = cookie_value.value
                else:
                    headers[key] = val
            http_request.headers = headers
            http_request.cookies = cookies

        user_name_password = curl.authentication
        if user_name_password:
            if ':' not in user_name_password:
                raise ValueError('Missing ":" in username header')
            base64_encoded = base64.b64encode(user_name_password.encode("ascii")).decode("utf-8")
            http_request.headers = http_request.headers or {}
            http_request.headers['Authorization'] = f'Basic {base64_encoded}'

        if curl.data:
            curl.method = 'POST'
            http_request.data = '&'.join(curl.data)

        if curl.method:
            curl.method = curl.method.upper()
            methods = {'HEAD', 'GET', 'DELETE', 'OPTIONS', 'PATCH', 'POST', 'PUT'}
            if curl.method not in methods:
                ValueError(f'Method {curl.method} is not a valid http method')
        else:
            curl.method = 'GET'

        if curl.insecure:
            http_request.insecure = True

        http_request.method = curl.method
        return http_request

    def parse(self) -> HttpRequest:
        """
        Main method to parse the curl command
        :return:
        """

        args = self.parse_args()
        return self.get_http_request(args)

    def parse_args(self):
        examples = """Examples:
            Enter a right curl command like 
            curl -H "Content-Type: application/json" -H "Authorization: 123" -X POST -d @mypostbody.json http://endpointurl.com/example
            """
        parser = argparse.ArgumentParser(description="CURL parser",
                                         epilog=examples)
        parser.add_argument('url')
        parser.add_argument('-H', '--header', dest='headers', action='append')
        parser.add_argument('-X', '--request', dest='method')
        parser.add_argument('-d', '--data', '--data-raw', dest='data', action='append')
        parser.add_argument('-u', '--user', dest='authentication')
        parser.add_argument('-k', '--insecure', dest='insecure', action='store_true')

        # todo fill others as well
        safe_to_ignore_n_0 = [
            [['--limit-rate'], 0],
            [['-r', '--range'], 1]
        ]
        for i, nargs in safe_to_ignore_n_0:
            if nargs:
                parser.add_argument(*i, nargs=nargs)
            else:
                parser.add_argument(*i, action='store_true', )
        parser.add_argument('-', action='store_true', dest='stdout')

        try:
            args = shlex.split(self.curl_command)[1:]
        except Exception as e:
            raise ValueError('Possible syntax error')
        try:
            curl_args, unknown = parser.parse_known_args(args)
            return curl_args
        except Exception as e:
            raise ValueError('Unknown argument passed')


def main():
    curl_command = 'curl -H "Content-Type: application/json" -H "Authorization:Basic token" -X POST -d "test body" --data-raw "test body2" http://example.com/example?a=1&b=2'

    curl_parser = CurlParser(curl_command)
    http_request = curl_parser.parse()
    print(http_request)


if __name__ == '__main__':
    main()

# todo
# will also work curl --data-urlencode "name=I am Daniel" http://www.example.com
# read this https://curl.se/docs/httpscripting.html
