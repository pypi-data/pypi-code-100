import unittest
from intentBox.utils import expand_parentheses
from intentBox.coreference import replace_coreferences
from intentBox import Segmenter


class TestIntentSyntax(unittest.TestCase):
    def test_expand(self):
        self.assertEqual(
            expand_parentheses("(hey|hello) world"),
            [['h', 'e', 'y', ' ', 'w', 'o', 'r', 'l', 'd'],
             ['h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd']])
        self.assertEqual(
            expand_parentheses("(hey|hello) world", as_strings=True),
            ['hey world', 'hello world'])
        self.assertEqual(
            expand_parentheses("(hey|hello) [world]", as_strings=True),
            ['hey world', 'hey ', 'hello world', 'hello '])

    def test_seg(self):
        s = Segmenter()
        self.assertEqual(
            s.segment("tell me a joke and say hello"),
            ['tell me a joke', 'say hello'])
        self.assertEqual(
            s.segment("turn off the lights, open the door"),
            ['turn off the lights', ' open the door'])
        self.assertEqual(
            s.segment("nice work! get me a beer"),
            ['nice work', ' get me a beer'])
        self.assertEqual(
            s.segment("tell me a joke and the weather"),
            ['tell me a joke', 'the weather'])

    def test_coref(self):
        self.assertEqual(
            replace_coreferences("call mom and tell her hello"),
            "call mom and tell mom hello")

        self.assertEqual(
            replace_coreferences("Here is the book now take it."),
            "Here is the book now take book .")
