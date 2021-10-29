# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""The ``forms`` module defines views forms for data entry and query
construction.

.. autosummary::
   :nosignatures:

   broker_web.apps.contact.forms.ContactForm
"""

from django import forms


class ContactForm(forms.Form):
    """Form to send a "contact us" email to the maintainers"""

    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
