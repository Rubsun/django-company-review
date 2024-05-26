from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework import status

from companies_app.models import Client, Company, Equipment

def create_test_with_auth(url, page_name, template, auth=True):
    def method(self):
        self.client = APIClient()
        if auth:
            self.user = User.objects.create_user(username='user', password='password')
            self.client_user = Client.objects.create(user=self.user)
            self.client.force_login(self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, template)

        response = self.client.get(reverse(page_name))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, template)

    return method

def create_test_no_auth(url):
    def method(self):
        self.client = APIClient()

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)

    return method

def create_test_instance(url, page_name, model, creation_attrs):
    def method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='user', password='password')
        self.client_user = Client.objects.create(user=self.user)
        self.client.force_login(self.user)

        creation_attrs['client'] = self.client_user
        instance = model.objects.create(**creation_attrs)

        response = self.client.get(reverse(page_name, args=[instance.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    return method

# required order: url, page name, template
pages = (
    ('/equipments/', 'equipments', 'pages/equipments.html'),
    ('/companies/', 'companies', 'pages/companies.html'),
    ('/profile/', 'profile', 'pages/profile.html'),
    ('/create_equipment/', 'create_equipment', 'pages/create_equipment.html'),
    ('/create_company/', 'create_company', 'pages/create_company.html'),

     )
base_pages = (
    ('/', 'homepage', 'index.html'),
    ('/register/', 'register', 'registration/register.html'),
    ('/login/', 'login', 'registration/login.html'),
)

methods = {f'test_{page[1]}': create_test_with_auth(*page) for page in (list(pages) + list(base_pages))}
TestPagesAuth = type('TestPagesAuth', (TestCase,), methods)

methods_no_auth = {f'test_{url}': create_test_no_auth(url) for url, _, _ in pages}
base_pages_no_auth = {f'test_{page[1]}': create_test_with_auth(*page, auth=False) for page in base_pages}
methods_no_auth.update(base_pages_no_auth)
TestPagesNoAuth = type('TestPagesNoAuth', (TestCase,), methods_no_auth)

instance_pages = (
    ('/company/', 'company_detail', Company, {'title': 'A', 'phone': '1234567890'}),
    ('/equipment/', 'equipment_view', Equipment, {'title': 'A', 'size': 10, 'category': None}),
)
methods_instance = {f'test_{page[1]}': create_test_instance(*page) for page in instance_pages}
TestInstancePages = type('TestInstancePages', (TestCase,), methods_instance)
