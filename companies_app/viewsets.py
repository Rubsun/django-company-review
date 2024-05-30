"""Contains viewsets for the API."""

from rest_framework import viewsets

from .permissions import APIPermission


def create_view_set(model_class, serializer):
    """
    Factory function to create custom ViewSets for Django REST Framework.

    Args:
        model_class: Model class.
        serializer: Serializer class.

    Returns:
        class: Custom ViewSet class.
    """
    class CustomViewSet(viewsets.ModelViewSet):
        queryset = model_class.objects.all()
        serializer_class = serializer
        permission_classes = [APIPermission]

    return CustomViewSet
