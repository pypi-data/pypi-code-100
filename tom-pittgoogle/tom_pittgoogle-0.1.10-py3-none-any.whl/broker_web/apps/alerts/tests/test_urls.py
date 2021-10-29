# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``urls`` module."""

from django.test import TestCase
from django.urls import resolve, reverse

from broker_web.apps.alerts import urls, views


class TestUrlRouting(TestCase):
    """Test URLs are routed to the correct views"""

    app_name = urls.app_name

    def test_alerts_json_routing(self):
        """Test 'alerts-json' is routed to``AlertsJsonView``"""

        url = reverse(f'{self.app_name}:alerts-json')
        self.assertEqual(views.AlertsJsonView, resolve(url).func.view_class)

    def test_recent_alerts_routing(self):
        """Test 'recent-alerts' is routed to``RecentAlertsView``"""

        url = reverse(f'{self.app_name}:recent-alerts')
        self.assertEqual(views.RecentAlertsView, resolve(url).func.view_class)

    def test_alert_summary_routing(self):
        """Test 'alert-summary' is routed to``AlertSummaryView``"""

        dummy_alert_pk = '123'
        url = reverse(f'{self.app_name}:alert-summary', args=[dummy_alert_pk])
        self.assertEqual(views.AlertSummaryView, resolve(url).func.view_class)
