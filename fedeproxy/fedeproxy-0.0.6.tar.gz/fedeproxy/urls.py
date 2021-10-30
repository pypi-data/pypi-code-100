"""fedeproxy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.urls import re_path
from django.views.generic import TemplateView

from fedeproxy.activitypub import regex
from fedeproxy.views import activitypub, hooks, wellknown

USER_PATH = r"^user/(?P<username>%s)" % regex.USERNAME
LOCAL_USER_PATH = r"^user/(?P<username>%s)" % regex.LOCALNAME

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="visitor/landing-index.html"), name="landing_index"),
    url(r"^accounts/", include("allauth.urls")),
    re_path(r"^\.well-known/nodeinfo/?$", wellknown.nodeinfo_pointer, name="wellknown-nodeinfo"),
    re_path(r"^nodeinfo/2\.0/?$", wellknown.nodeinfo),
    re_path(r"^inbox/?$", activitypub.inbox),
    re_path(r"^hook/project/(?P<namespace>[^/]+)/(?P<project>[^/]+)/?$", hooks.hook, name="hook_project"),
    re_path(r"^hook/system/?$", hooks.hook, name="hook_system"),
    re_path(r"%s/inbox/?$" % LOCAL_USER_PATH, activitypub.inbox, name="inbox"),
    re_path(r"%s/outbox/?$" % LOCAL_USER_PATH, activitypub.outbox),
    re_path(r"%s/?$" % USER_PATH, activitypub.user, name="user"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
