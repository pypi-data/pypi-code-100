# -*- coding: utf-8 -*-
import unittest
from dynamic_url import Url


class TestParams(unittest.TestCase):
    array_test = ["Origin"]
    dict_test = {"Origin": "test"}
    dict_test2 = {"Not_Origin": "test"}
    dict_test3 = {"Origin": "https://www.google.com/"}
    dict_test4 = {"Origin": ""}

    def test_get_url_two_params(self):
        self.assertEqual(
            Url().get_url("hola", "db"), "", "Error in params -> two strings"
        )
        self.assertEqual(
            Url().get_url("", ""), "", "Error in params -> two empty strings"
        )

    def test_get_url_array_params(self):
        self.assertEqual(
            Url().get_url(self.array_test, "db"),
            "",
            "Error in params with array",
        )

    def test_get_url_dict_params(self):
        self.assertEqual(
            Url().get_url(self.dict_test, "db"),
            "",
            "Error in params with array",
        )
        self.assertEqual(
            Url().get_url(self.dict_test2, db={"db": ""}),
            "",
            "Error in params with array",
        )
        self.assertEqual(
            Url().get_url(self.dict_test3, "db"),
            "",
            "Error in params with array",
        )
        self.assertEqual(
            Url().get_url(self.dict_test4, "db"),
            "",
            "Error in params with array",
        )


if __name__ == "__main__":
    unittest.main()
