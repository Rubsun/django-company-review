"""Tests for api."""
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from companies_app.models import Company, Equipment, Review


def create_apitest(model_class, model_url, creation_attrs):
    """
    Create API test case for a specific model.

    Args:
        model_class (class): The model class to be tested.
        model_url (str): The URL endpoint for the model's API.
        creation_attrs (dict): Dictionary containing attr for creating an instance of the model.

    Returns:
        class: A test case class for testing the API endpoints of the specified model.
    """

    class APITest(TestCase):
        _user_creds = {'username': 'test', 'password': 'defpass'}
        _superuser_creds = {'username': 'admin', 'password': 'adminpass', 'is_superuser': True}

        def setUp(self):
            """Set up the test environment by creating users and tokens."""
            self.client = APIClient()
            self.user = User.objects.create_user(**self._user_creds)
            self.user_token = Token.objects.create(user=self.user)
            self.superuser = User.objects.create_superuser(**self._superuser_creds)
            self.superuser_token = Token.objects.create(user=self.superuser)

        def get(self, user: User, token: Token):
            """
            Test GET request to the API.

            Args:
                user: The user making the request.
                token: The token associated with the user.
            """
            self.client.force_authenticate(user=user, token=token)
            response = self.client.get(model_url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_get_user(self):
            """Test GET request to the API by a regular user."""
            self.get(self.user, self.user_token)

        def test_get_superuser(self):
            """Test GET request to the API by a superuser."""
            self.get(self.superuser, self.superuser_token)

        def manage(self, user, token, post_status: int, put_status: int, delete_status: int):
            """
            Test managing API resources (POST, PUT, DELETE).

            Args:
                user (User): The user making the request.
                token (Token): The token associated with the user.
                post_status (int): Expected status code for POST request.
                put_status (int): Expected status code for PUT request.
                delete_status (int): Expected status code for DELETE request.
            """
            self.client.force_authenticate(user=user, token=token)

            # POST
            response = self.client.post(model_url, creation_attrs)
            self.assertEqual(response.status_code, post_status)

            # creating object for changes
            created = model_class.objects.create(**creation_attrs)
            url = f'{model_url}{created.id}/'

            # PUT
            response = self.client.put(url, creation_attrs)
            self.assertEqual(response.status_code, put_status)

            # DELETE
            response = self.client.delete(url)
            self.assertEqual(response.status_code, delete_status)

        def test_manage_user(self):
            """Test managing API resources by a regular user."""
            self.manage(
                self.user, self.user_token, status.HTTP_403_FORBIDDEN, status.HTTP_403_FORBIDDEN,
                status.HTTP_403_FORBIDDEN,
            )

        def test_manage_superuser(self):
            """Test managing API resources by a superuser."""
            self.manage(
                self.superuser, self.superuser_token, status.HTTP_201_CREATED, status.HTTP_200_OK,
                status.HTTP_204_NO_CONTENT,
            )

    return APITest


CompanyApiTest = create_apitest(
    Company,
    '/api/companies/',
    {
        'title': 'Test Company',
        'phone': '123-456-7890',
    },
)
EquipmentApiTest = create_apitest(
    Equipment, '/api/equipment/', {'title': 'Test Equipment', 'size': 10},
)
ReviewApiTest = create_apitest(Review, '/api/review/', {'text': 'Test Review', 'rating': 5})
