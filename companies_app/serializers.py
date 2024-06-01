"""
Serializers for the companies application.

Defines serializers for:
- Company
- Equipment
- Review
"""

from rest_framework import serializers

from .models import Company, Equipment, Review


class CompanySerializer(serializers.ModelSerializer):
    """Serializer for the Company model."""

    class Meta:
        """Meta class."""

        model = Company
        fields = '__all__'


class EquipmentSerializer(serializers.ModelSerializer):
    """Serializer for the Equipment model."""

    class Meta:
        """Meta class."""

        model = Equipment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for the Review model."""

    class Meta:
        """Meta class."""

        model = Review
        fields = '__all__'
