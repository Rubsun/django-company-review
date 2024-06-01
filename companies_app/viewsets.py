"""Contains viewsets for the API."""

from rest_framework import viewsets

from .permissions import APIPermission


def create_view_set(model_class, serializer):
    """
    Create custom ViewSets for Django REST Framework.

    Args:
        model_class: Model class.
        serializer: Serializer class.

    Returns:
        class: Custom ViewSet class.
    """
    class CustomViewSet(viewsets.ModelViewSet):
        """Custom ViewSets for Django REST Framework."""

        queryset = model_class.objects.all()
        serializer_class = serializer
        permission_classes = [APIPermission]

    return CustomViewSet
