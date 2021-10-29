# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``views`` module."""

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from broker_web.apps.subscriptions import urls

User = get_user_model()


class GenericTests:
    """Tests that are applicable to multiple views"""

    def test_unauthenticated_get(self):
        """Test ``get`` method returns correct template with 200 status code"""

        # Define the url for the view, and the login url that the user should
        # be redirected to for being unauthenticated.
        view_url = reverse(self.url_name)
        login_url = reverse('login') + '?next=' + view_url

        response = Client().get(view_url)
        self.assertEqual(302, response.status_code)
        self.assertEqual(login_url, response.url)

    def test_authenticated_get(self):
        """Test ``get`` method returns correct template with 200 status code"""

        test_user = User.objects.get_or_create(email='user@email.com')[0]
        client = Client()
        client.force_login(test_user)

        url = reverse(self.url_name)
        response = client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, self.template)


class SubscriptionsView(TestCase, GenericTests):
    """Tests for the ``Subscriptions`` view"""

    url_name = f'{urls.app_name}:subscriptions'
    template = 'subscriptions/subscriptions.html'


class ProfileView(TestCase, GenericTests):
    """Tests for the ``Profile`` view"""

    url_name = f'{urls.app_name}:profile'
    template = 'subscriptions/my_profile.html'
