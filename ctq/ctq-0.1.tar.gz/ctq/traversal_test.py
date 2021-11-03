from .traversal import get_root
from .traversal import resource_path_names
from .traversal import traverse_up
from unittest import TestCase


class Node(object):
    pass


class TestTraversal(TestCase):
    def setUp(self):
        self.root = Node()

        self.mid = Node()
        self.mid.__name__ = "mid"
        self.mid.__parent__ = self.root

        self.leaf = Node()
        self.leaf.__name__ = "leaf"
        self.leaf.__parent__ = self.mid

    def test_traverse_up(self):
        result = [getattr(a, "__name__", None) for a in traverse_up(self.leaf)]
        self.assertEqual(result, ["leaf", "mid", None])

    def test_path_names(self):
        result = resource_path_names(self.leaf)
        self.assertEqual(result, ("", "mid", "leaf"))

    def test_get_root(self):
        result = get_root(self.leaf)
        self.assertEqual(result, self.root)
