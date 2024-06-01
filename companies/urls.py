"""Urls for companies app."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('companies_app.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
