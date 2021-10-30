from resourcerer import get_resources
from resourcerer.parse_yaml import get_yaml_obj
import unittest
import os


class TestDownload(unittest.TestCase):

    def setUp(self) -> None:
        os.chdir("test")
        self.yaml_path = "resources.yaml"
        resources = get_yaml_obj(self.yaml_path)
        self.path = os.path.join(
            resources["target_folder"],
            resources['test_resources'][0])

    def test_download(self):
        get_resources.main(self.yaml_path)
        self.assertTrue(os.path.exists(self.path))

    def tearDown(self) -> None:
        os.remove(self.path)
        os.chdir("..")


if __name__ == "__main__":
    unittest.main()
