"""
URL configuration for the companies application.

Includes routes for:
- Homepage
- API endpoints for companies, equipment, and reviews
- User registration, login, and logout
- Profile viewing by user ID
- Equipment and company management
"""
from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('companies', views.CompanyViewSet)
router.register('equipment', views.EquipmentViewSet)
router.register('review', views.ReviewViewSet)

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('api/', include(router.urls)),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/<int:user_id>/', views.profile_view_by_id, name='profile_by_id'),
    path('equipments/', views.equipments_view, name='equipments'),
    path('equipment/<uuid:equipment_id>/', views.equipment_view, name='equipment_view'),
    path('equipment/<uuid:equipment_id>/delete/', views.delete_equipment, name='delete_equipment'),
    path('companies/', views.companies_view, name='companies'),
    path('company/<uuid:company_id>/', views.company_detail_view, name='company_detail'),
    path('create_company/', views.create_company, name='create_company'),
    path('create_equipment/', views.create_equipment, name='create_equipment'),
    path(
        'add_equipment_to_company/<uuid:equipment_id>/',
        views.add_equipment_to_company,
        name='add_equipment_to_company',
    ),
    path('delete_review/<uuid:review_id>/', views.delete_review, name='delete_review'),
    path('delete_company/<uuid:company_id>/', views.delete_company, name='delete_company'),
]
