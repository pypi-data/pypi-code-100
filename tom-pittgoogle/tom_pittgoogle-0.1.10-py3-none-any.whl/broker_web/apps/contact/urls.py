# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""The ``urls`` module configures routes from URLs to views.

+--------------------+----------------------------+---------------------------+
| URL                | View                       | name                      |
+====================+============================+===========================+
|``/``               | ``ContactView``            | ``contact``               |
+--------------------+----------------------------+---------------------------+
|``sent``            | ``SuccessView``            | ``contact-sent``          |
+--------------------+----------------------------+---------------------------+
"""

from django.urls import path

from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.ContactView.as_view(), name='contact'),
    path('sent', views.SuccessView, name='contact-sent'),
]
