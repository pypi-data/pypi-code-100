# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://api_docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'broker_web.main.settings')

application = get_asgi_application()
