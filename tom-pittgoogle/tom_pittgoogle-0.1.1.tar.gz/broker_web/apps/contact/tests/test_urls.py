# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``urls`` module."""

from django.test import TestCase
from django.urls import resolve, reverse

from broker_web.apps.contact import urls, views


class TestUrlRouting(TestCase):
    """Test URLs are routed to the correct views"""

    app_name = urls.app_name

    def test_contact_routing(self):
        """Test 'contact' is routed to``ContactView``"""

        url = reverse(f'{self.app_name}:contact')
        self.assertEqual(views.ContactView, resolve(url).func.view_class)

    def test_contact_sent_routing(self):
        """Test 'contact-sent' is routed to``success_view``"""

        url = reverse(f'{self.app_name}:contact-sent')
        self.assertEqual(views.SuccessView, resolve(url).func)
