# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""The ``views`` module defines ``View`` objects for converting web requests
into rendered responses.

.. autosummary::
   :nosignatures:

   broker_web.apps.contact.views.ContactView
"""

from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from .forms import ContactForm

SuccessView = TemplateView.as_view(template_name='contact/contact_sent.html')


class ContactView(FormView):
    """View for submitting an email to the website maintainers"""

    template_name = "contact/contact_us.html"
    form_class = ContactForm
    # Todo: Include app name in reverse lookup in case app is namespaced differently
    success_url = reverse_lazy('contact:contact-sent')

    def form_valid(self, form):
        """Send contents of email form and redirect to success url

        Called after form is validated

        Args:
            form (django.forms.Form): User creation form
        """

        subject = form.cleaned_data['subject']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        try:
            send_mail(subject, message, email, settings.CONTACT_EMAILS)

        except BadHeaderError:
            return HttpResponse('Invalid header found.')

        return super().form_valid(form)
