from resourcerer import send_resources
from resourcerer.get_from_onedrive import _obtain_download_link
from resourcerer.shared import CLIENT_ID, TENANT_ID, SITE_ID, auth_token
from resourcerer.parse_yaml import get_yaml_obj
from resourcerer.delete_from_onedrive import delete_from_onedrive
import unittest
import os
import glob
import time


class TestUpload(unittest.TestCase):

    def setUp(self) -> None:
        os.chdir("test")
        self.yaml_path = "resources.yaml"
        self.resources = get_yaml_obj(self.yaml_path)
        self.path = os.path.join(
            self.resources["target_folder"],
            self.resources['uploadables'][0])
        self.to_delete_from_onedrive = os.path.join(
            self.resources['source_folder'],
            glob.glob(self.resources['uploadables'][0])[0]
        ).replace("\\", "/")

    def test_upload(self):
        send_resources.main(self.yaml_path)
        url = _obtain_download_link(
            auth_token(CLIENT_ID, TENANT_ID),
            SITE_ID,
            self.to_delete_from_onedrive
        )
        self.assertIsNotNone(url)

    def tearDown(self) -> None:
        os.chdir("..")
        time.sleep(10)
        delete_from_onedrive(
            auth_token(CLIENT_ID, TENANT_ID),
            SITE_ID,
            self.to_delete_from_onedrive
        )


if __name__ == "__main__":
    unittest.main()
