# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""The ``views`` module defines ``View`` objects for converting web requests
into rendered responses.

.. autosummary::
   :nosignatures:

   broker_web.apps.subscriptions.views.ProfileView
   broker_web.apps.subscriptions.views.SubscriptionsView
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import View


class SubscriptionsView(LoginRequiredMixin, View):
    """View that handles new user subscriptions"""

    def get(self, request, *args, **kwargs):
        return render(request, 'subscriptions/subscriptions.html')


class ProfileView(LoginRequiredMixin, View):
    """View that handles user profiles"""

    def get(self, request, *args, **kwargs):
        """Handle an incoming HTTP request

        Args:
            request (HttpRequest): Incoming HTTP request

        Returns:
            Outgoing HTTPResponse
        """

        # Todo get pubsub messages
        timestamps = [123, 456]
        messages = ['a', 'b']
        context = {
            'pbsub_zip': zip(timestamps, messages)
        }

        return render(request, 'subscriptions/my_profile.html', context)
