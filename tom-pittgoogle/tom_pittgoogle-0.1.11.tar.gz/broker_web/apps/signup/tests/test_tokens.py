# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``urls`` module."""

from django.test import TestCase

from broker_web.apps.signup import tokens
from broker_web.apps.signup.models import CustomUser


class TestTokenGenerator(TestCase):
    """Tests for the account activation token generator"""

    def setUp(self):
        """Create a test user to generate a token for"""

        # pk is used when calculating the token and so must be set
        self.test_user = CustomUser(pk=1)
        self.token_generator = tokens.TokenGenerator()

    def test_valid_token(self):
        """Test generated token is identified as invalid"""

        valid_token = self.token_generator.make_token(self.test_user)
        is_valid = self.token_generator.check_token(self.test_user, valid_token)
        self.assertTrue(is_valid)

    def test_invalid_token(self):
        """Test dummy token is identified as invalid"""

        invalid_token = 'not a token'
        is_valid = self.token_generator.check_token(self.test_user, invalid_token)
        self.assertFalse(is_valid)

    def test_user_token_is_unique(self):
        """Test tokens are unique even when generated for different users"""

        token1 = self.token_generator.make_token(self.test_user)

        self.test_user.pk += 10
        token2 = self.token_generator.make_token(self.test_user)

        self.assertNotEqual(token1, token2)
