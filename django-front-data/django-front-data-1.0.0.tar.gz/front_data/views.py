from .models import FrontData, FAQ
from .serializers import FullFrontDataSerializer, FrontDataSerializer, FAQSerializer, StdFrontDataSerializer

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
