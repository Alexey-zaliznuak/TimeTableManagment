from rest_framework import permissions


class MethodistOrCanEditAllOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, editable):
        return request.user.can_edit_all

class CanEditAllOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, role_object):
        return request.user.can_edit_all

class YourRoleOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, role_object):
        return (
            request.user == role_object.user
            or request.user.can_edit_all
        )
