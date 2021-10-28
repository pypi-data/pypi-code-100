# !/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""URL routing for the main django application. URLS from each application
is routed to the following namespaces:

+-------------------------+---------------------+
| Application             | Namespace           |
+=========================+=====================+
|``apps.alerts``          | ``alerts``          |
+-------------------------+---------------------+
|``apps.contact``         | ``contact``         |
+-------------------------+---------------------+
|``apps.getting_started`` | ``getting-started`` |
+-------------------------+---------------------+
|``apps.objects``         | ``objects``         |
+-------------------------+---------------------+
|``apps.signup``          | ``signup``          |
+-------------------------+---------------------+
|``apps.subscriptions``   | ``subscriptions``   |
+-------------------------+---------------------+
"""

from django.contrib import admin
from django.urls import include
from django.urls import path

from .views import IndexView, why_pgb_view

urlpatterns = [
    # URLs for custom views
    path('', IndexView.as_view(), name='home'),
    path('why_pgb/', why_pgb_view, name='why-pgb'),
    path('contact/', include('broker_web.apps.contact.urls', namespace='contact')),
    path('alerts/', include('broker_web.apps.alerts.urls', namespace='alerts')),
    path('objects/', include('broker_web.apps.objects.urls', namespace='objects')),
    path('getting_started/', include('broker_web.apps.getting_started.urls', namespace='getting-started')),
    path('signup/', include('broker_web.apps.signup.urls', namespace='signup')),
    path('subscriptions/', include('broker_web.apps.subscriptions.urls', namespace='subscriptions')),

    # Built in Django URL patterns
    path('users/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls)
]

# Error handling
handler404 = 'broker_web.apps.error_pages.views.error_404'
handler500 = 'broker_web.apps.error_pages.views.error_500'
