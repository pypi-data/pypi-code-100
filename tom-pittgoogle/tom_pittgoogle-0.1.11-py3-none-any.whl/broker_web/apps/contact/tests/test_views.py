# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Tests for the ``views`` module."""

from django.test import TestCase
from django.urls import reverse

from broker_web.apps.contact import urls, views
from broker_web.apps.contact.forms import ContactForm


class ContactView(TestCase):
    """Tests for the ``Contact`` view"""

    url_name = f'{urls.app_name}:contact'
    template = 'contact/contact_us.html'

    success_url_name = f'{urls.app_name}:contact-sent'
    success_template = 'contact/contact_sent.html'

    def test_get(self):
        """Test ``get`` method returns correct template"""

        url = reverse(self.url_name)
        response = self.client.post(url)

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, self.template)

    def test_form_valid_redirect(self):
        """Test ``form_valid`` method redirects to correct success URL"""

        self.assertEqual(
            self.success_template,
            ContactView.success_template,
            'Incorrect success template')

        valid_form = ContactForm(data=dict(
            email='test@email.com',
            subject='Test Name',
            message='Test message.'
        ))

        valid_form.is_valid()  # to set the form's ``cleaned_data`` attribute
        view = views.ContactView()
        response = view.form_valid(valid_form)
        self.assertEqual(302, response.status_code, 'Status code is not 302 redirect')

        success_url = reverse(self.success_url_name)
        self.assertEqual(success_url, response.url)


class SuccessView(TestCase):
    """Tests for the ``success_view`` view"""

    url_name = f'{urls.app_name}:contact-sent'
    template = 'contact/contact_sent.html'

    def test_get(self):
        """Test ``get`` method returns correct template"""

        url = reverse(self.url_name)
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, self.template)
