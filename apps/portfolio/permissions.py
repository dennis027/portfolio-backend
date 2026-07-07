from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """Anyone can GET; only staff (Django admin) can write. Used for all
    the reference-data endpoints (projects, skills, experience, etc.)."""

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
