from rest_framework.permissions import BasePermission


class ProjectPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            return (request.user.has_perm('projects.change_project') or
                    request.user.has_perm('projects.change_project', view.project))

        return True

    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            return (request.user.has_perm('projects.change_project') or
                    request.user.has_perm('projects.change_project', view.project))

        return False
