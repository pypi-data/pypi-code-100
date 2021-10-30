from django.urls import path
from django.core.exceptions import ImproperlyConfigured
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from slunic import hooks
from slunic.configs import app_configs

hooks.search_for_hooks()

viewset_hooks = hooks.get_hooks(app_configs.API_VIEWSETS_HOOK_V1)
apiview_hooks = hooks.get_hooks(app_configs.API_VIEWS_HOOK_V1)


def get_router():
    router = DefaultRouter()
    for hook in viewset_hooks:
        name, viewset, basename = hook()
        router.register("%s" % name, viewset, basename)
    return router


def get_apiview():
    urlpatterns = []
    for hook in apiview_hooks:
        url_path, apiview, name = hook()
        if not issubclass(apiview, APIView):
            raise ImproperlyConfigured("%s must subclass of DRF APIView")
        if name:
            url = path(url_path, apiview.as_view(), name=name)
        else:
            url = path(url_path, apiview.as_view(), name=apiview.__class__.__name__.lower())
        urlpatterns.append(url)
    return urlpatterns


app_name = "v1"

urlpatterns = get_apiview() + get_router().urls
