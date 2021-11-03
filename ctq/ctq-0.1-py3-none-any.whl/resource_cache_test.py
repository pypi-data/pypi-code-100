# -*- coding:utf-8 -*-

from .resource_cache import ResourceCache
from unittest import TestCase


class TestResource(TestCase):
    def setUp(self):
        self.resource = ResourceCache()

    def test_cache(self):
        res = self.resource

        # Check no value
        result = res.resource_cache_get(("foo",))
        self.assertIsNone(result)

        # Check set
        item = object()
        res.resource_cache_set(("bar",), item)
        result = res.resource_cache_get(("bar",))
        self.assertIs(result, item)

        # Check clear
        res.resource_cache_clear()
        result = res.resource_cache_get(("bar",))
        self.assertIsNone(result)
