# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``forms`` module."""

from django.test import TestCase

from broker_web.apps.objects.forms import FilterObjectsForm


class TestFilterObjectsForm(TestCase):
    """Test the ``FilterObjectsForm`` validates correctly"""

    def test_empty_form(self):
        """Test that an empty form is valid"""

        form = FilterObjectsForm(data={})
        self.assertTrue(form.is_valid())
