# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``urls`` module."""

from django.test import TestCase
from django.urls import resolve, reverse

from broker_web.apps.getting_started import urls, views


class TestUrlRouting(TestCase):
    """Test URLs are routed to the correct views"""

    app_name = urls.app_name

    def test_introduction_routing(self):
        """Test 'introduction' is routed to ``Introduction``"""

        url = reverse(f'{self.app_name}:introduction')
        self.assertEqual(views.Introduction, resolve(url).func)

    def test_data_products_routing(self):
        """Test 'data-products' is routed to ``DataProducts``"""

        url = reverse(f'{self.app_name}:data-products')
        self.assertEqual(views.DataProducts, resolve(url).func)

    def test_technical_resources_routing(self):
        """Test 'technical-resources' is routed to ``TechnicalResources``"""

        url = reverse(f'{self.app_name}:technical-resources')
        self.assertEqual(views.TechnicalResources, resolve(url).func)

    def test_data_access_routing(self):
        """Test 'data-access' is routed to ``DataAccess``"""

        url = reverse(f'{self.app_name}:data-access')
        self.assertEqual(views.DataAccess, resolve(url).func)

    def test_broker_design_routing(self):
        """Test 'broker-design' is routed to ``BrokerDesign``"""

        url = reverse(f'{self.app_name}:broker-design')
        self.assertEqual(views.BrokerDesign, resolve(url).func)

