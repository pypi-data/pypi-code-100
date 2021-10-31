# pylint: skip-file
import asyncio
import unittest

from fastapi.testclient import TestClient
from ioc.exc import UnsatisfiedDependency

from .. import ResourceEndpointSet
from .. import __boot__ as boot
from ..asgi import Application


class BearerAuthorizationTestCase(unittest.TestCase):

    class view_class(ResourceEndpointSet):

        async def create(self):
            pass

        async def index(self):
            pass

        async def retrieve(self, resource_id):
            pass

    def setUp(self):
        asyncio.run(boot.on_setup())
        self.app = Application(
            allowed_hosts=['*'],
            enable_debug_endpoints=True
        )
        self.client = TestClient(self.app)
        self.view_class.add_to_router(self.app, '/test')

    def get_token(self, claims: dict = None):
        response = self.client.post('/debug/token', json=claims or {})
        return response.text

    def test_retrieve_unauthenticated(self):
        response = self.client.get('/test/1')
        self.assertEqual(response.status_code, 401, response.text)

    def test_retrieve_authenticated(self):
        headers = {'Authorization': f'Bearer {self.get_token()}'}
        response = self.client.get('/test/1', headers=headers)
        self.assertEqual(response.status_code, 200, response.text)

    def test_retrieve_expired(self):
        token = self.get_token({'exp': 1})
        headers = {'Authorization': f'Bearer {token}'}
        response = self.client.get('/test/1', headers=headers)
        dto = response.json()
        self.assertEqual(response.status_code, 403, response.text)
        self.assertIn('code', dto)
        self.assertEqual(dto['code'], 'CREDENTIAL_EXPIRED')

    def test_create_unauthenticated(self):
        response = self.client.post('/test')
        self.assertEqual(response.status_code, 401, response.text)

    def test_create_authenticated(self):
        headers = {'Authorization': f'Bearer {self.get_token()}'}
        response = self.client.post('/test', headers=headers)
        self.assertEqual(response.status_code, 200, response.text)

    def test_create_expired(self):
        token = self.get_token({'exp': 1})
        headers = {'Authorization': f'Bearer {token}'}
        response = self.client.post('/test', headers=headers)
        dto = response.json()
        self.assertEqual(response.status_code, 403, response.text)
        self.assertIn('code', dto)
        self.assertEqual(dto['code'], 'CREDENTIAL_EXPIRED')

    def test_index_unauthenticated(self):
        response = self.client.get('/test')
        self.assertEqual(response.status_code, 401, response.text)

    def test_index_authenticated(self):
        headers = {'Authorization': f'Bearer {self.get_token()}'}
        response = self.client.get('/test', headers=headers)
        self.assertEqual(response.status_code, 200, response.text)

    def test_index_expired(self):
        token = self.get_token({'exp': 1})
        headers = {'Authorization': f'Bearer {token}'}
        response = self.client.get('/test', headers=headers)
        dto = response.json()
        self.assertEqual(response.status_code, 403, response.text)
        self.assertIn('code', dto)
        self.assertEqual(dto['code'], 'CREDENTIAL_EXPIRED')

