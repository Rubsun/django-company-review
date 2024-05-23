from django.contrib import admin
from .models import Company, CompanyEquipment, Review, Equipment, Client, Category, Address
from django.utils.translation import gettext_lazy as _


class EquipmentInline(admin.TabularInline):
    model = Equipment
    extra = 1

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

class ClientInline(admin.TabularInline):
    model = Client
    extra = 1


class CompanyEquipmentInline(admin.TabularInline):
    model = CompanyEquipment
    extra = 1


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    model = Address

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    model = Company
    inlines = [CompanyEquipmentInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    inlines = [EquipmentInline]


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    model = Equipment
    inlines = [CompanyEquipmentInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    model = Review

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    model = Client
    inlines = [ReviewInline]