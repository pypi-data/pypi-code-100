from requestgen.generator.language_java import (apache_http_client,
                                                http_url_connection)
from requestgen.generator.language_python import python_generator
from requestgen.generator.curl import curl_generator

from requestgen.beans import http_request as req


to_languages_mapping = {'PYTHON_REQUESTS': python_generator.PythonGenerator,
                        'JAVA_APACHE_HTTP_CLIENT': apache_http_client.ApacheHttpClientCodeGenerator,
                        'JAVA_HTTP_URL_CONNECTION': http_url_connection.HttpUrlConnectionGenerator,
                        'CURL': curl_generator.CurlGenerator}


class CodeGenerator:

    def __init__(self, to_language):
        self.code_generator = to_languages_mapping.get(to_language)
        if not self.code_generator:
            message = f'Language {to_language} not supported\n'
            l = [key for key in to_languages_mapping.keys()]
            message += f'Supported languages to convert to are {", ".join(l)}'
            raise ValueError(message)

    def generate(self, http_request):
        validate_input(http_request)
        generator = self.code_generator(http_request)
        code = generator.generate_code()
        return code

def validate_input(http_object):
    assert http_object.url, 'URL can\'t be empty'
    assert http_object.method, 'method can\'t be empty'


def generate(to_language, http_request):
    generator = CodeGenerator(to_language=to_language)
    return generator.generate(http_request)

def main():
    http_request = req.HttpRequest()
    http_request.url = 'test.com'
    http_request.method = 'GET'
    http_request.headers = {'key1': 'va1', 'key2': 'val2'}
    http_request.data = 'this is a test body'
    http_request.cookies = {'c_key1': 'va1', 'c_key2': 'val2'}
    print(generate('PYTHON_REQUESTS', http_request))


if __name__ == '__main__':
    main()
