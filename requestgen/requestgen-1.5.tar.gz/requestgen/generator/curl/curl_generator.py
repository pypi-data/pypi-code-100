from requestgen.beans.http_request import HttpRequest
from requestgen.generator.generator import Generator
from requestgen.parser.curl_parser import CurlParser


class CurlGenerator(Generator):
    cookies_template = "cookies = {{\n{text}}}"
    headers_template = "headers = {{\n{text}}}"
    data_template = "data = '{text}'"
    tab = '    '

    def __init__(self, http_request):
        super().__init__(http_request)

    def generate_headers(self):
        d = self.http_request.headers
        if not d:
            return
        # self.code += ' \\\n'
        for key, val in d.items():
            self.code += f" \\\n-H '{key}:{val}'"

    def init_curl_url_and_method(self):
        method = self.http_request.method

        self.code += 'curl '
        if self.http_request.insecure:
            self.code += '-k '
        self.code += f'-X {method} '
        self.code += f"'{self.http_request.url}'"

    def generate_data(self):
        if not self.http_request.data:
            return
        self.code += ' \\\n'
        self.code += f'-d \'{self.http_request.data}\''

    def generate_code(self):
        self.sanitize_input()
        self.init_curl_url_and_method()
        self.generate_headers()
        self.generate_data()
        return self.code

    def check_insecure_connection(self):
        if self.http_request.insecure:
            result = '''
// You have specified -k or --insecure in the input request
// Please follow the steps to enable it
// https://stackoverflow.com/questions/1201048/allowing-java-to-use-an-untrusted-certificate-for-ssl-https-connection'''
            self.add(result)


def main():
    http_request = HttpRequest()
    http_request.insecure = True
    http_request.method = 'POST'
    http_request.url = 'http://test.com'
    # http_request.data = 'test'
    # http_request.headers = {'a': 'b', 'x': 'y'}
    generator = CurlGenerator(http_request)
    code = generator.generate_code()
    print(code)
    pass


if __name__ == '__main__':
    main()

# todo Improvements
# curl -o myfile.css https://cdn.keycdn.com/css/animate.min.css download this file and save it
