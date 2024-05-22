from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from . import views

router = DefaultRouter()
router.register('companies', views.CompanyViewSet)
router.register('equipment', views.EquipmentViewSet)
router.register('review', views.ReviewViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('register/', views.register, name='register'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('equipment/<uuid:equipment_id>/', views.equipment_view, name='equipment_view'),
    path('', views.homepage, name='homepage'),
    path('companies/', views.companies_view, name='companies'),
    path('company/<uuid:company_id>/', views.company_detail_view, name='company_detail'),
    path('equipments/', views.equipments_view, name='equipments'),
]
