"""
Admin configuration for the companies application.

Registers the following models with the admin site:
- Address
- Company
- Category
- Equipment
- Review
- Client

Defines inlines for related models.
"""

from django.contrib import admin

from .models import (Address, Category, Client, Company, CompanyEquipment,
                     Equipment, Review)


class EquipmentInline(admin.TabularInline):
    """Inline for equipment related to a category."""

    model = Equipment
    extra = 1


class ReviewInline(admin.TabularInline):
    """Inline for reviews related to a client."""

    model = Review
    extra = 1


class ClientInline(admin.TabularInline):
    """Inline for clients."""

    model = Client
    extra = 1


class CompanyEquipmentInline(admin.TabularInline):
    """Inline for equipment related to a company."""

    model = CompanyEquipment
    extra = 1


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """Admin configuration for the Address model."""

    model = Address


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Admin configuration for the Company model."""

    model = Company
    inlines = [CompanyEquipmentInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for the Category model."""

    model = Category
    inlines = [EquipmentInline]


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    """Admin configuration for the Equipment model."""

    model = Equipment
    inlines = [CompanyEquipmentInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin configuration for the Review model."""

    model = Review


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """Admin configuration for the Client model."""

    model = Client
    inlines = [ReviewInline]
