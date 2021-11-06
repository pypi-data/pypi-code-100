from typing import Any

from .models import FrontData, FAQ, Configuration
from .serializers import FullFrontDataSerializer, FrontDataSerializer, FAQSerializer, StdFrontDataSerializer, \
    ConfigurationSerializer

try:
    from rest_framework import viewsets, permissions
    from rest_framework.filters import SearchFilter


    class FrontDataViewSet(viewsets.ModelViewSet):
        filter_backends = [SearchFilter]
        search_fields = ['name', 'data']
        permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
        queryset = FrontData.objects.all()
        serializer_class = FrontDataSerializer


    class StdFrontDataViewSet(FrontDataViewSet):
        permission_classes = [permissions.DjangoModelPermissions]
        search_fields = ['name', 'data', 'templates']
        serializer_class = StdFrontDataSerializer


    class FullFrontDataViewSet(StdFrontDataViewSet):
        serializer_class = FullFrontDataSerializer


    class FAQViewSet(viewsets.ModelViewSet):
        permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
        queryset = FAQ.objects.all()
        serializer_class = FAQSerializer
        filter_backends = [SearchFilter]
        search_fields = ['question', 'answer']


    class ConfigurationViewSet(viewsets.ModelViewSet):
        permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
        queryset = Configuration.objects.all()
        serializer_class = ConfigurationSerializer
        filter_backends = [SearchFilter]
        search_fields = ['key', 'value', 'description']
except (ModuleNotFoundError, ImportError):
    class FAQViewSet:
        """Don't use this. Install djangorestframework before using this"""
        pass


    class FrontDataViewSet:
        """Don't use this. Install djangorestframework before using this"""
        pass


    class StdFrontDataViewSet:
        """Don't use this. Install djangorestframework before using this"""
        pass


    class FullFrontDataViewSet:
        """Don't use this. Install djangorestframework before using this"""
        pass

    class ConfigurationViewSet:
        """Don't use this. Install djangorestframework before using this"""
        pass


def get_configuration(key: str) -> str | None:
    """
    Get a configuration value by key.

    :param key: The key of the configuration value.
    :return: The value of the configuration value. None if the key is not found.
    """
    try:
        return Configuration.objects.get(key=key).value
    except Configuration.DoesNotExist:
        return None


def set_configuration(key: str, value: Any, description='') -> None:
    """
    Set a configuration value by key.

    :param description: Description of the configuration.
    :param key: The key of the configuration value.
    :param value: The value of the configuration value.
    """
    value = str(value)
    try:
        config = Configuration.objects.get(key=key)
        config.value = value
        if description:
            config.description = description
        config.save()
    except Configuration.DoesNotExist:
        config = Configuration(key=key, value=value)
        if description:
            config.description = description
        config.save()
