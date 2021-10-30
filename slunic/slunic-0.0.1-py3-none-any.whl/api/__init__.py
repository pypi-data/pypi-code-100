from .v1.urls import get_router

default_app_config = "slunic.api.apps.AppConfig"

DEFAULT_ROUTER = get_router()
DEFAULT_VIEWSETS = {model_name: viewset for model_name, viewset, _ in DEFAULT_ROUTER.registry}
