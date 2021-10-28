# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``views`` module."""

from django.test import Client, TestCase
from django.urls import reverse

from broker_web.apps.getting_started import urls


class TestTemplates(TestCase):
    """Test views use the correct templates"""

    app_name = urls.app_name

    def setUp(self):
        self.client = Client()

    def test_introduction_template(self):
        """Test ``Introduction`` view uses the correct template"""

        url = reverse(f'{self.app_name}:introduction')
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'getting_started/introduction.html')

    def test_data_products_template(self):
        """Test ``DataProducts`` view uses the correct template"""

        url = reverse(f'{self.app_name}:data-products')
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'getting_started/data_products.html')

    def test_technical_resources_template(self):
        """Test ``TechnicalResources`` view uses the correct template"""

        url = reverse(f'{self.app_name}:technical-resources')
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'getting_started/technical_resources.html')

    def test_data_access_template(self):
        """Test ``DataAccess`` view uses the correct template"""

        url = reverse(f'{self.app_name}:data-access')
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'getting_started/data_access.html')

    def test_broker_design_template(self):
        """Test ``BrokerDesign`` view uses the correct template"""

        url = reverse(f'{self.app_name}:broker-design')
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'getting_started/broker_design.html')
