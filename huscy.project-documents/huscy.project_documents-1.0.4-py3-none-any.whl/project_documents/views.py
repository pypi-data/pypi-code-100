from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

from huscy.projects.models import Project
from huscy.project_documents import serializer, services
from huscy.project_documents.permissions import ProjectPermissions


class DocumentViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, ProjectPermissions)
    serializer_class = serializer.DocumentSerializer

    def initial(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        super().initial(request, *args, **kwargs)

    def get_queryset(self):
        return services.get_documents(self.project)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['project'] = self.project
        return context


class DocumentTypeViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                          mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = (DjangoModelPermissions, )
    queryset = services.get_document_types()
    serializer_class = serializer.DocumentTypeSerializer

    def perform_destroy(self, document_type):
        services.delete_document_type(document_type)
