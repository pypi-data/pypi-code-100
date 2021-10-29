# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``forms`` module."""

from django.test import TestCase

from broker_web.apps.signup.forms import CustomUserChangeForm, CustomUserCreationForm


class TestCustomUserCreationForm(TestCase):
    """Test the ``CustomUserCreationForm`` validates correctly"""

    def test_empty_form(self):
        """Test that an empty form is invalid"""

        form = CustomUserCreationForm(data={})
        self.assertFalse(form.is_valid())


class TestCustomUserChangeForm(TestCase):
    """Test the ``CustomUserChangeForm`` validates correctly"""

    def test_empty_form(self):
        """Test that an empty form is invalid"""

        form = CustomUserChangeForm(data={})
        self.assertFalse(form.is_valid())