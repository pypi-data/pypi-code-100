# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Defines views for converting a Web requests into a Web responses"""

from django.shortcuts import render
from django.views.generic import TemplateView, View

why_pgb_view = TemplateView.as_view(template_name='broker_web/why_pgb.html')


class IndexView(View):
    """View for the index page"""

    def get(self, request):
        """Handle an incoming HTTP request

        Args:
            request (HttpRequest): Incoming HTTP request

        Returns:
            Outgoing HTTPResponse
        """

        context = {
            'online': False
        }

        return render(request, 'broker_web/index.html', context)
