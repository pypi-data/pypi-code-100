# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``forms`` module."""

from django.test import TestCase

from broker_web.apps.contact.forms import ContactForm


class TestContactForm(TestCase):
    """Test the ``ContactForm`` validates correctly"""

    def test_valid_form(self):
        """Test a full form is valid invalid"""

        form = ContactForm(data=dict(
            email='test@email.com',
            name='Test Name',
            message='Test message.'
        ))
        self.assertFalse(form.is_valid())

    def test_invalid_email(self):
        """Test email validation is enforced"""

        form = ContactForm(data=dict(
            email='invalid_email',
            name='Test Name',
            message='Test message.'
        ))
        self.assertFalse(form.is_valid())

    def test_empty_form(self):
        """Test an empty form is invalid"""

        form = ContactForm(data=dict(
            email='',
            name='',
            message=''
        ))
        self.assertFalse(form.is_valid())
