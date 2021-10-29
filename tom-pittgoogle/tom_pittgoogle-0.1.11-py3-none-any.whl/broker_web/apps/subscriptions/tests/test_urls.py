# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``urls`` module."""

from django.test import TestCase
from django.urls import resolve, reverse

from broker_web.apps.subscriptions import urls, views


class TestUrlRouting(TestCase):
    """Test URLs are routed to the correct views"""

    app_name = urls.app_name

    def test_subscriptions_routing(self):
        """Test 'subscriptions' is routed to``SubscriptionsView``"""

        url = reverse(f'{self.app_name}:subscriptions')
        self.assertEqual(views.SubscriptionsView, resolve(url).func.view_class)

    def test_profile_routing(self):
        """Test 'profile' is routed to``ProfileView``"""

        url = reverse(f'{self.app_name}:profile')
        self.assertEqual(views.ProfileView, resolve(url).func.view_class)
