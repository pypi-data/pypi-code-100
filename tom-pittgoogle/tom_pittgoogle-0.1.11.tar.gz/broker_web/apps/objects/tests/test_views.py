# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``views`` module."""

from django.http import JsonResponse
from django.test import Client, TestCase
from django.urls import reverse

from broker_web.apps.objects import urls


class ObjectsJsonView(TestCase):
    """Tests for the ``ObjectsJsonView`` view"""

    url_name = f'{urls.app_name}:objects-json'
    app_name = urls.app_name

    def setUp(self):
        self.client = Client()

    def test_get_returns_json(self):
        """Test ``get`` method returns Json Response"""

        url = reverse(self.url_name)
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response, JsonResponse)


class RecentObjectsView(TestCase):
    """Tests for the ``RecentObjects`` view"""

    url_name = f'{urls.app_name}:recent-objects'
    template = 'objects/recent_objects.html'

    def setUp(self):
        self.client = Client()

    def test_get(self):
        """Test ``get`` method returns correct template"""

        url = reverse(self.url_name)
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, self.template)

    def test_post(self):  # Todo: Add filtering from form and update tests
        """Test ``post`` method returns correct template"""

        url = reverse(self.url_name)
        response = self.client.post(url)

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, self.template)


class RecentAlertsJsonView(TestCase):
    """Tests for the ``RecentAlertsJsonView`` view"""

    url_name = f'{urls.app_name}:single-object-json'
    app_name = urls.app_name

    def setUp(self):
        self.client = Client()

    def test_get_returns_json(self):
        """Test ``get`` method returns Json Response"""

        url = reverse(self.url_name, kwargs={'pk': 'dummy_id_name'})
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response, JsonResponse)


class ObjectSummaryView(TestCase):
    """Tests for the ``ObjectSummary`` view"""

    url_name = f'{urls.app_name}:object-summary'
    template = 'objects/object_summary.html'

    def setUp(self):
        self.client = Client()

    def test_get(self):
        """Test ``get`` method returns correct template and object id"""

        dummy_object_id = '123'
        url = reverse(self.url_name, args=[dummy_object_id])
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, self.template)

        returned_object_id = response.context['object_id']
        self.assertEqual(returned_object_id, dummy_object_id)
