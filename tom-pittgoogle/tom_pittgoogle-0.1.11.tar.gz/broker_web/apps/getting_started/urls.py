# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""The ``urls`` module configures routes from URLs to views.

+------------------------+--------------------------+-------------------------+
| URL                    | View                     | name                    |
+========================+==========================+=========================+
|``/``                   | ``Introduction``         | ``introduction``        |
+------------------------+--------------------------+-------------------------+
|``data_products``       | ``DataProducts``         | ``data-products``       |
+------------------------+--------------------------+-------------------------+
|``technical_resources`` | ``TechnicalResources``   | ``technical-resources`` |
+------------------------+--------------------------+-------------------------+
|``data_access``         | ``DataAccess``           | ``data-access``         |
+------------------------+--------------------------+-------------------------+
|``broker_design``       | ``BrokerDesign``         | ``broker-design``       |
+------------------------+--------------------------+-------------------------+
"""

from django.urls import path

from . import views

app_name = 'getting_started'

urlpatterns = [
    path('', views.Introduction, name='introduction'),
    path('data_products', views.DataProducts, name='data-products'),
    path('technical_resources', views.TechnicalResources, name='technical-resources'),
    path('data_access', views.DataAccess, name='data-access'),
    path('broker_design', views.BrokerDesign, name='broker-design'),
]
