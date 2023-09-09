from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # everybody can exec GET, HEAD, OPTIONS request
        if request.method in permissions.SAFE_METHODS:
            return True
        # admin can exec post delete put .ect request
        return request.user.is_superuser
