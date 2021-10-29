# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``urls`` module."""

from django.test import TestCase
from django.urls import resolve, reverse

from broker_web.apps.signup import urls, views


class TestUrlRouting(TestCase):
    """Test URLs are routed to the correct views"""

    app_name = urls.app_name

    def test_signup_routing(self):
        """Test 'signup' is routed to``SignUp``"""

        url = reverse(f'{self.app_name}:signup')
        self.assertEqual(views.SignUp, resolve(url).func.view_class)

    def test_activation_sent_routing(self):
        """Test 'activation-sent' is routed to``activation_sent_view``"""

        url = reverse(f'{self.app_name}:activation-sent')
        self.assertEqual(views.ActivationSentView, resolve(url).func)

    def test_activate_routing(self):
        """Test 'activate' is routed to``ActivateAccount``"""

        # noinspection SpellCheckingInspection
        dummy_activation_key = {'uidb64': 'AB', 'token': 'CDE-FGHIJK'}
        url = reverse(f'{self.app_name}:activate', kwargs=dummy_activation_key)
        self.assertEqual(views.ActivateAccount, resolve(url).func.view_class)
