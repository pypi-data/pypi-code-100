# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""The ``urls`` module configures routes from URLs to views.

+----------------------+----------------------------+-------------------------+
| URL                  | View                       | name                    |
+======================+============================+=========================+
|``/``                 | ``SignUp``                 | ``signup``              |
+----------------------+----------------------------+-------------------------+
|``activation_sent``   | ``ActivationSentView``     | ``activation-sent``     |
+----------------------+----------------------------+-------------------------+
|``[AUTH-TOKEN-LINK]`` | ``ActivateAccount``        | ``activate``            |
+----------------------+----------------------------+-------------------------+
"""

from django.urls import path, re_path

from .views import ActivateAccount, SignUp, ActivationSentView

app_name = 'signup'
activation_token_regex = r'(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$'

urlpatterns = [
    path('', SignUp.as_view(), name='signup'),
    path('activation_sent', ActivationSentView, name='activation-sent'),
    re_path(activation_token_regex, ActivateAccount.as_view(), name='activate'),
]
