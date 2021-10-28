from pathlib import Path

import httpx
from pyupdater.core.uploader import BaseUploader


class HTTPUploader(BaseUploader):
    name = 'HTTPUploader'
    author = '@cybergrind'

    def init_config(self, config):
        self.server_url = config['server_url']
        self.data_params = config.get('data_params', {})
        self.filename_param = config.get('filename_param', '')

    def set_config(self, config):
        server_name = self.get_answer("Please enter server name\n--> ")
        config["server_url"] = server_name
        config['data_params'] = {}

    def upload_file(self, filename):
        files = {'file': open(filename, 'rb')}
        data = {**self.data_params}
        if self.filename_param:
            data[self.filename_param] = Path(filename).name
        r = httpx.post(self.server_url, files=files, data=data)
        r.raise_for_status()
