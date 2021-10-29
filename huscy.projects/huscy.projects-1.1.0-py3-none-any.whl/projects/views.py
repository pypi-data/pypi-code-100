import logging

from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated, IsAdminUser
from reversion import set_comment
from reversion.views import RevisionMixin

from huscy.projects import serializer, services
from huscy.projects.models import Project
from huscy.projects.permissions import IsProjectCoordinator, ProjectPermission, ReadOnly

logger = logging.getLogger('projects')


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class MembershipViewSet(RevisionMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                        mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializer.MembershipSerializer
    permission_classes = (IsAuthenticated, IsAdminUser | IsProjectCoordinator | ReadOnly)

    def initial(self, request, *args, **kwargs):
        self.project = get_object_or_404(Project, pk=self.kwargs['project_pk'])
        super().initial(request, *args, **kwargs)

    def get_queryset(self):
        return services.get_memberships(self.project)

    def perform_create(self, serializer):
        membership = serializer.save(project=self.project)
        set_comment('Created membership <ID-{membership.id}> for project <ID-{self.project.id}>')

        logger.info('Membership created by user %s from IP %s for project "%s" and member %s',
                    self.request.user.username, get_client_ip(self.request),
                    membership.project.title, membership.user.get_full_name())

    def perform_destroy(self, membership):
        services.delete_membership(membership)
        set_comment('Deleted membership <ID-{membership.id}>')

        logger.info('Membership deleted by user %s from IP %s for project "%s" and member %s',
                    self.request.user.username, get_client_ip(self.request),
                    membership.project.title, membership.user.get_full_name())

    def perform_update(self, serializer):
        membership = serializer.save()
        set_comment('Updated membership <ID-{membership.id}>')

        logger.info('Membership updated by user %s from IP %s for project "%s" and member %s',
                    self.request.user.username, get_client_ip(self.request),
                    membership.project.title, membership.user.get_full_name())


class ProjectViewSet(RevisionMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                     mixins.ListModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializer.ProjectSerializer
    permission_classes = (IsAuthenticated, ProjectPermission)

    def get_queryset(self):
        return services.get_projects()

    def perform_create(self, serializer):
        project = serializer.save()
        set_comment(f'Created project <ID-{project.id}>')

        logger.info('Project created by user %s from IP %s with title "%s"',
                    self.request.user.username, get_client_ip(self.request), project.title)

    def perform_destroy(self, project):
        services.delete_project(project)
        set_comment(f'Deleted project <ID-{project.id}>')

        logger.info('Project deleted by user %s from IP %s with title "%s"',
                    self.request.user.username, get_client_ip(self.request), project.title)

    def perform_update(self, serializer):
        project = serializer.save()
        set_comment(f'Updated project <ID-{project.id}>')

        logger.info('Project updated by user %s from IP %s with title "%s"',
                    self.request.user.username, get_client_ip(self.request), project.title)


class ResearchUnitViewSet(RevisionMixin, viewsets.ModelViewSet):
    permission_classes = (DjangoModelPermissions, )
    queryset = services.get_research_units()
    serializer_class = serializer.ResearchUnitSerializer

    def perform_create(self, serializer):
        research_unit = serializer.save()
        set_comment(f'Created research unit <ID-{research_unit.id}>')

    def perform_destroy(self, research_unit):
        research_unit.delete()
        set_comment(f'Deleted research unit <ID-{research_unit.id}>')

    def perform_update(self, serializer):
        research_unit = serializer.save()
        set_comment(f'Updated research unit <ID-{research_unit.id}>')
