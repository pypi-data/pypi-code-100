# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``urls`` module."""

from django.test import TestCase
from django.urls import resolve, reverse

from broker_web.apps.alerts import views
from broker_web.apps.objects import urls, views


class TestUrlRouting(TestCase):
    """Test URLs are routed to the correct views"""

    app_name = urls.app_name

    def test_objects_json_routing(self):
        """Test 'objects-json' is routed to``ObjectsJsonView``"""

        url = reverse(f'{self.app_name}:objects-json')
        self.assertEqual(views.RecentObjectsJsonView, resolve(url).func.view_class)

    def test_recent_objects_routing(self):
        """Test 'recent-objects' is routed to``RecentObjectsView``"""

        url = reverse(f'{self.app_name}:recent-objects')
        self.assertEqual(views.RecentObjectsView, resolve(url).func.view_class)

    def test_object_summary_routing(self):
        """Test 'object-summary' is routed to``ObjectSummaryView``"""

        dummy_alert_pk = '123'
        url = reverse(f'{self.app_name}:object-summary', args=[dummy_alert_pk])
        self.assertEqual(views.ObjectSummaryView, resolve(url).func.view_class)
