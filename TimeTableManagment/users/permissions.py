from rest_framework import permissions


class SelfOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.can_edit_all
            or request.user == obj.user
        )
