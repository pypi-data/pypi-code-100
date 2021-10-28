from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

from huscy.projects.models import Project
from huscy.project_ethics import serializer
from huscy.project_ethics.models import Ethic
from huscy.project_ethics.permissions import EthicFilePermission, EthicPermission
from huscy.project_ethics.services import get_ethic_boards, get_ethic_files, get_ethics


class EthicBoardViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                        mixins.UpdateModelMixin, viewsets.GenericViewSet):
    http_method_names = 'delete', 'head', 'get', 'options', 'post', 'put'
    permission_classes = (DjangoModelPermissions, )
    queryset = get_ethic_boards()
    serializer_class = serializer.EthicBoardSerializer


class EthicViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                   mixins.UpdateModelMixin, viewsets.GenericViewSet):
    http_method_names = 'delete', 'head', 'get', 'options', 'post', 'put'
    permission_classes = IsAuthenticated, EthicPermission
    serializer_class = serializer.EthicSerializer

    def initial(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        super().initial(request, *args, **kwargs)

    def get_queryset(self):
        return get_ethics(self.project)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['project'] = self.project
        return context


class EthicFileViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin,
                       viewsets.GenericViewSet):
    http_method_names = 'delete', 'head', 'options', 'post', 'put'
    permission_classes = IsAuthenticated, EthicFilePermission

    def initial(self, request, *args, **kwargs):
        self.ethic = get_object_or_404(Ethic.objects.select_related('project'),
                                       pk=self.kwargs['ethic_pk'],
                                       project=self.kwargs['project_pk'])
        super().initial(request, *args, **kwargs)

    def get_queryset(self):
        return get_ethic_files(self.ethic)

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return serializer.UpdateEthicFileSerializer
        return serializer.EthicFileSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['ethic'] = self.ethic
        return context
