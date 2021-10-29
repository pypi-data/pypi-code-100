# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``views`` module."""

from django.test import Client, TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from broker_web.apps.signup import models, tokens, urls


class TestSignUpView(TestCase):
    """Tests for the ``SignUp`` view"""

    url_name = f'{urls.app_name}:signup'
    template = 'signup/create_new_user.html'

    def setUp(self):
        self.client = Client()

    def test_get(self):
        """Test ``get`` method returns correct template and object id"""

        url = reverse(self.url_name)
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, self.template)


class TestActivateAccount(TestCase):
    """Tests for the ``ActivateAccount`` view"""

    url_name = f'{urls.app_name}:activate'
    invalid_token_template = 'signup/invalid_activation_link.html'
    valid_token_template = 'signup/activation_success.html'

    def setUp(self):
        # Create client and test user
        self.client = Client()
        self.test_user = models.CustomUser(pk=1)

        # Create activation token for custom user
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.test_user.pk))
        self.test_token = tokens.account_activation_token.make_token(self.test_user)

    def test_get_with_invalid_token(self):
        """Test get request with invalid token redirects to invalid token page"""

        # noinspection SpellCheckingInspection
        bad_signup_token = {'uidb64': 'AB', 'token': 'CDE-FGHIJK'}
        url = reverse(self.url_name, kwargs=bad_signup_token)
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, self.invalid_token_template)

    def test_get_with_valid_token(self):
        """Test get request with invalid token redirects to success page"""

        good_signup_token = {'uidb64': self.uidb64, 'token': self.test_token}
        url = reverse(self.url_name, kwargs=good_signup_token)
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, self.valid_token_template)
