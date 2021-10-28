# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""Web Server Gateway Interface configuration

This module exposes the WSGI callable as a module-level variable named
``application``.

For more information on this file, see
https://api_docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'broker_web.main.settings')

application = get_wsgi_application()
