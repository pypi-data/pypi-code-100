from rest_framework.permissions import BasePermission


class ChangeSubjectPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_perm('subjects.change_subject')


class NotePermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.has_perm('subjects.change_subject'):
            return True

        if request.method == 'POST':
            return request.user.has_perm('subjects.add_note')

        return False

    def has_object_permission(self, request, view, note):
        if request.method == 'DELETE':
            if request.user.has_perm('subjects.change_subject'):
                return (request.user.has_perm('subjects.delete_note') or
                        request.user.has_perm('subjects.delete_note', note))
        return True


class ViewSubjectPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.is_authenticated and request.user.has_perm('subjects.view_subject')
        return True
