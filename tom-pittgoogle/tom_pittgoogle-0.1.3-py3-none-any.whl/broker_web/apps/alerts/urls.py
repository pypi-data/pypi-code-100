# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""The ``urls`` module configures routes from URLs to views.

+--------------------+----------------------------+---------------------------+
| URL                | View                       | name                      |
+====================+============================+===========================+
|``/``               | ``RecentAlertsView``       | ``recent-alerts``         |
+--------------------+----------------------------+---------------------------+
|``<str:pk>``        | ``AlertSummaryView``       | ``alert-summary``         |
+--------------------+----------------------------+---------------------------+
|``json/``           | ``AlertsJsonView``         | ``alerts-json``           |
+--------------------+----------------------------+---------------------------+
"""

from django.urls import path

from . import views

app_name = 'alerts'

urlpatterns = [
    path('', views.RecentAlertsView.as_view(), name='recent-alerts'),
    path('<str:pk>', views.AlertSummaryView.as_view(), name='alert-summary'),
    path('json/', views.AlertsJsonView.as_view(), name='alerts-json'),
]
