import unittest
from setuptools import find_packages

class TestNote(unittest.TestCase):
    def test_set_note(self):
        test_note = Note()
        test_note.set_note(100, 'C', 5, 0, 10)
        self.assertEquals(test_note.get_note_data(), [100, 'C', 5, 0, 10, 10], "Note should be a C5, lasting ten seconds, at velocity level 100.")
        return
        