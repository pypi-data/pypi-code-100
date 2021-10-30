from rest_framework.permissions import BasePermission
import slunic.permissions as perms

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")


class IsAdminOrReadOnly(BasePermission):
    """
    The request is as a staff or superuser, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or perms.is_admin(request.user))


class IsTutorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return perms.is_tutor(request.user)


class IsNotPageAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author != request.user


class IsAuthorOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        admin = request.user.is_staff or request.user.is_superuser
        author = obj.author == request.user
        return author or admin
