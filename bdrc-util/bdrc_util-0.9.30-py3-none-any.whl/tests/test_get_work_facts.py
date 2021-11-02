import unittest
import tempfile

import os
from pathlib import Path

from util_lib.utils import get_work_facts, get_work_image_facts

test_temp_dir: object
work1_name: str = "Work1"


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        """
        Create some files
        :return:
        """
        # Make a test root
        global test_temp_dir, work1_name
        test_temp_dir = tempfile.TemporaryDirectory()
        w1 = Path(test_temp_dir.name, work1_name)
        w1arc = Path(str(w1), 'archive')
        w1img = Path(str(w1), 'images')
        os.mkdir(w1)
        os.mkdir(w1arc)
        os.mkdir(w1img)
        with open(Path(w1arc, "W1Archive1File1"), "w") as wa1:
            wa1.write("0123456789")
        fp = open(Path(w1arc, "empty"), "w")
        fp.close()

        with open(Path(w1img, "W1imageFile1"), "w") as wa1:
            wa1.write("01234567890123456789")

    def test_util_work_facts(self):
        global test_temp_dir, work1_name
        facts = get_work_facts(str(Path(test_temp_dir.name, work1_name)))

        #  total size should be 30
        self.assertEqual(facts[0], 30)

        # in 3 files
        self.assertEqual(facts[1], 3)

    def test_util_work_image_facts(self):
        global test_temp_dir, work1_name
        facts = get_work_image_facts(str(Path(test_temp_dir.name, work1_name)))

        #  total non image size is 10, in 2 files
        self.assertEqual(facts[0], 10, "non image size not correct")

        # in 3 files
        self.assertEqual(facts[1], 2, "non-image file count not correct")

        # total image size is 20, in one file
        self.assertEqual(facts[2], 20, "image file size not correct")
        self.assertEqual(facts[3], 1, "image file count not correct")


if __name__ == '__main__':
    unittest.main()
