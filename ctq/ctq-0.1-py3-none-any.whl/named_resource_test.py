from .named_resource import iter_named_resources
from .named_resource import resource
from .named_resource import Resourceful
from unittest import TestCase
from unittest.mock import MagicMock


class Root(Resourceful):
    @resource("mid")
    def get_mid(self):
        return Mid()

    @resource("mid-no-cache", no_cache=True)
    def get_mid_no_cache(self):
        return Mid()

    @resource("mid-no-parent", no_parent=True)
    def get_mid_no_parent(self):
        return Mid()

    @resource("my-leaf")
    def get_my_leaf(self):
        return self["mid"]["leaf"]


class Mid(Resourceful):
    @resource("leaf")
    def get_leaf(self):
        return Leaf()


class Leaf(object):
    pass


class TestNamedResource(TestCase):
    def setUp(self):
        self.root = Root()

    def test_get(self):
        r = self.root
        self.assertIsInstance(r["mid"], Mid)
        self.assertIsInstance(r["mid"]["leaf"], Leaf)
        self.assertIsInstance(r.get_mid(), Mid)
        self.assertIsInstance(r["mid"].get_leaf(), Leaf)
        with self.assertRaises(KeyError):
            r["foo"]

    def test_cache(self):
        r = self.root
        self.assertIs(r["mid"], r["mid"])
        self.assertIsNot(r["mid-no-cache"], r["mid-no-cache"])

    def test_binding(self):
        r = self.root
        mid = r["mid"]
        self.assertEqual(mid.__parent__, r)
        self.assertEqual(mid.__name__, "mid")

        mid_no_parent = r["mid-no-parent"]
        self.assertFalse(hasattr(mid_no_parent, "__parent__"))
        self.assertFalse(hasattr(mid_no_parent, "__name__"))

    def test_proxied(self):
        r = self.root
        my_leaf = r["my-leaf"]
        self.assertIsInstance(my_leaf, Leaf)
        self.assertEqual(my_leaf.__parent__, r["mid"])
        self.assertEqual(my_leaf.__name__, "leaf")

    def test_iter_named_resources(self):
        resources = iter_named_resources(self.root)
        self.assertEqual(
            [getattr(a, "__name__", None) for a in resources],
            [
                "mid",
                "mid-no-cache",
                None,
                "leaf",
            ],
        )

    def test_root_caching_get(self):
        self.root.resource_cache_get = MagicMock()
        mid = self.root["mid"]
        self.assertIs(
            mid,
            self.root.resource_cache_get.return_value,
        )
        self.root.resource_cache_get.assert_called_with(("", "mid"))

    def test_root_caching_set(self):
        self.root.resource_cache_set = MagicMock()
        mid = self.root["mid"]
        self.root.resource_cache_set.assert_called_with(("", "mid"), mid)
