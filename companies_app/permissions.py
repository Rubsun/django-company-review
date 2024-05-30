"""Contains custom permission classes for the API."""

from rest_framework import permissions


class APIPermission(permissions.BasePermission):
    """
    Custom permission class for API endpoints.

    Allows GET requests for authenticated users and superusers.
    Disallows POST, PUT, and DELETE requests for non-superusers.
    """

    _allowed_methods = ['GET', 'OPTIONS', 'HEAD']
    _not_allowed_methods = ['POST', 'PUT', 'DELETE']

    def has_permission(self, request, view):
        """
        Check if the user has permission to access the endpoint.

        Args:
            request: Request object.
            view: View object.

        Returns:
            bool: True if user has permission, False otherwise.
        """
        if request.method in self._allowed_methods and request.user.is_authenticated:
            return True
        if request.method in self._not_allowed_methods and request.user.is_superuser:
            return True
        return False
