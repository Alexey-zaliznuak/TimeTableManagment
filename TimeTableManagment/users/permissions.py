from rest_framework import permissions


class UsersPermission(permissions.BasePermission):
    def has_permission(self, request, view) -> bool:
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, editable):
        editor = request.user
        if editor.can_edit_all_users:
            return True

        return editor.is_methodist and not editable.is_methodist
