from collections import OrderedDict

from rebotics_sdk.providers import ReboticsBaseProvider, remote_service


class FVMProvider(ReboticsBaseProvider):
    def set_retailer_identifier(self, codename: str, secret_key: str) -> None:
        self.headers['HTTP_X_RETAILER_CODENAME'] = codename
        self.headers['HTTP_X_RETAILER_SECRET_KEY'] = secret_key

    @remote_service('/api/synchronization/')
    def send_products_file_to_fvm(self, retailer_codename: str, products_count: int, file_url: str) -> OrderedDict:
        json = {
            'retailer_codename': retailer_codename,
            'products_count': products_count,
            'file': file_url
        }
        return self.session.post(data=json)

    @remote_service('/api/token-auth/')
    def token_auth(self, username, password, verification_code=None):
        payload = dict(
            username=username,
            password=password,
        )
        if verification_code is not None:
            payload['verification_code'] = verification_code

        json_data = self.session.post(data=payload)
        self.headers['Authorization'] = 'Token %s' % json_data['token']
        return json_data

    @remote_service('/api/files/virtual/')
    def create_virtual_upload(self, filename, pk):
        return self.session.post(
            pk=pk,
            json={
                "filename": filename
            }
        )

    @remote_service('/api/files/{pk}/finish/')
    def finish(self, pk):
        return self.session.post(pk=pk)
