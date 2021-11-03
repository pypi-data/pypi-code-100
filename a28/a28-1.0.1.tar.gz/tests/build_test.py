import contextlib
import os
import tempfile
import unittest
from argparse import Namespace
from io import StringIO

from a28.build import build


class TestAccountMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = tempfile.TemporaryDirectory()
        self.temp_stdout = StringIO()
        self.test_package_path = f'{os.path.dirname(__file__)}/fixtures/fake-pkg'

    def tearDown(self) -> None:
        self.test_dir.cleanup()

    def test_successful_build(self):
        with contextlib.redirect_stdout(self.temp_stdout):
            build(Namespace(src=self.test_package_path, dest=self.test_dir.name))

        self.assertEqual(
            f'{self.test_dir.name}/e3c02b90-3513-4742-81c5-fefa3abee637-0.1.0.a28',
            self.temp_stdout.getvalue().strip()
        )

    def test_successful_build_new_folder(self):
        with contextlib.redirect_stdout(self.temp_stdout):
            build(Namespace(src=self.test_package_path, dest=f'{self.test_dir.name}/newfolder'))

        self.assertEqual(
            f'{self.test_dir.name}/newfolder/e3c02b90-3513-4742-81c5-fefa3abee637-0.1.0.a28',
            self.temp_stdout.getvalue().strip()
        )
