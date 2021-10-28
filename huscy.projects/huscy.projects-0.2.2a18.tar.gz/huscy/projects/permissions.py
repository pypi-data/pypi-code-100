from rest_framework.permissions import BasePermission, SAFE_METHODS
from huscy.projects.models import Membership


class IsProjectCoordinator(BasePermission):
    def has_permission(self, request, view):
        return Membership.objects.filter(project=view.project, user=request.user,
                                         is_coordinator=True).exists()


class IsProjectMember(BasePermission):
    def has_permission(self, request, view):
        return Membership.objects.filter(project=view.project, user=request.user).exists()


class ProjectPermission(BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return (request.user.has_perm('projects.delete_project') or
                    request.user.has_perm('projects.delete_project', obj))

        if request.method in ['PATCH', 'PUT']:
            return (request.user.has_perm('projects.change_project') or
                    request.user.has_perm('projects.change_project', obj))


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
