import json
import os
import pytest
import glob


@pytest.fixture
def smartctl(monkeypatch):
    config = {'fixture': 'fixtures'}

    def load_smartctl_output(*args):
        args = '_'.join(args)
        args = args.replace('/', '_')
        data = open(os.path.join(os.path.dirname(__file__),
                                 config['fixture'],
                                 'smartctl',f'smartctl_{args}.json')).read()
        return json.loads(data)
    monkeypatch.setattr('fc.disktracker.local.smartctl', load_smartctl_output)
    return config


@pytest.fixture
def mock_api(monkeypatch, request):

    class API:

        def _get_responses_json_list(self, responses_path):
            responses_filenames = sorted(
                glob.glob(os.path.join(responses_path, '*')),
                reverse=True)

            responses_json_list = []

            for entry in responses_filenames:
                data = open(os.path.join(responses_path, entry)).read()
                data_json = json.loads(data)
                responses_json_list.append(data_json)
            return responses_json_list

        def __init__(self, url, token):
            self.url = url
            self.token = token
            self.request_number = 1

            responses_path = os.path.join(
                os.path.dirname(__file__), 'fixtures', request.node.name)
            self.responses = self._get_responses_json_list(responses_path)

        def get(self, path, **params):
            return self.request('get', path, **params)

        def post(self, path, **params):
            request = self.request('post', path, **params)
            try:
                return request['payload']
            except KeyError:
                return request

        def delete(self, path, **params):
            return self.request('delete', path, **params)

        def request(self, method, path, **params):
            # Print is used to debug the fixture.
            print(f'{self.request_number}. '
                  'request is: {method}, {path}, {params}')
            self.request_number += 1
            return self.responses.pop()

    monkeypatch.setattr('fc.disktracker.snipeit.API', API)
