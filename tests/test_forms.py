"""Tests for forms."""
from django.contrib.auth.models import User
from django.test import TestCase

from companies_app.forms import (CompanyForm, EquipmentForm, LoginForm,
                                 RegistrationForm, ReviewForm)
from companies_app.models import Category, Client, Equipment


class RegistrationFormTest(TestCase):
    """Test case for the RegistrationForm."""

    _valid_data = {
        'username': 'username',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email@email.com',
        'password1': 'Azpm1029!',
        'password2': 'Azpm1029!',
    }

    def test_valid(self):
        """Test valid registration form data."""
        self.assertTrue(RegistrationForm(data=self._valid_data).is_valid())

    def invalid(self, invalid_data):
        """
        Test invalid registration form data.

        Args:
            invalid_data (tuple): A tuple containing field-value pairs of invalid data.
        """
        valid_data = self._valid_data.copy()
        for field, value_data in invalid_data:
            valid_data[field] = value_data
        self.assertFalse(RegistrationForm(data=valid_data).is_valid())

    def test_short_password(self):
        """Test registration form with short password."""
        self.invalid(
            (
                ('password1', 'abc'),
                ('password2', 'abc'),
            ),
        )

    def test_common_password(self):
        """Test registration form with common password."""
        self.invalid(
            (
                ('password1', 'abcdef123'),
                ('password2', 'abcdef123'),
            ),
        )

    def test_different_passwords(self):
        """Test registration form with different passwords."""
        self.invalid(
            (
                ('password1', 'ASDksdjn9734'),
                ('password2', 'LKKJdfnalnd234329'),
            ),
        )

    def test_invalid_email(self):
        """Test registration form with invalid email."""
        self.invalid(
            (
                ('email', 'abc'),
            ),
        )

    def test_existing_user(self):
        """Test registration form with existing user."""
        username, password = 'username', 'password'
        User.objects.create(username=username, password=password)
        self.invalid(
            (
                ('username', username),
                ('password', password),
            ),
        )


class LoginFormTest(TestCase):
    """Test case for the LoginForm."""

    def test_valid(self):
        """Test valid login form data."""
        User.objects.create_user(username='testuser', password='password')
        form = LoginForm(data={'username': 'testuser', 'password': 'password'})
        self.assertTrue(form.is_valid())

    def test_invalid(self):
        """Test invalid login form data."""
        form = LoginForm(data={'username': '', 'password': 'wrongpassword'})
        self.assertFalse(form.is_valid())


class ReviewFormTest(TestCase):
    """Test case for the ReviewForm."""

    def setUp(self):
        """Set up the test environment by creating a user, a client, and an equipment instance."""
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client_model = Client.objects.create(user=self.user)
        self.equipment = Equipment.objects.create(
            title='Test Equipment',
            client=self.client_model,
            category=Category.objects.create(title='Test Category'),
        )

    def test_valid(self):
        """Test valid review form data."""
        form = ReviewForm(
            data={
                'text': 'Great equipment!',
                'rating': 5,
                'client': self.client_model,
                'equipment': self.equipment,
            },
        )
        self.assertTrue(form.is_valid())

    def test_invalid(self):
        """Test invalid review form data."""
        form = ReviewForm(
            data={
                'text': '', 'rating': 5,
                'client': self.client_model,
                'equipment': self.equipment,
            },
        )
        self.assertFalse(form.is_valid())


class CompanyFormTest(TestCase):
    """Test case for the CompanyForm."""

    def test_valid(self):
        """Test valid company form data."""
        form = CompanyForm(data={'title': 'Test Company', 'phone': '1234567890'})
        self.assertTrue(form.is_valid())

    def test_invalid(self):
        """Test invalid company form data."""
        form = CompanyForm(data={'title': '', 'phone': '1234567890'})
        self.assertFalse(form.is_valid())


class EquipmentFormTest(TestCase):
    """Test case for the EquipmentForm."""

    def setUp(self):
        """Set up the test environment by creating a category instance."""
        self.category = Category.objects.create(title='Test Category')

    def test_valid(self):
        """Test valid equipment form data."""
        form = EquipmentForm(
            data={'title': 'Test Equipment', 'size': 10, 'category': self.category.id},
        )
        self.assertTrue(form.is_valid())

    def test_invalid(self):
        """Test invalid equipment form data."""
        form = EquipmentForm(data={'title': '', 'size': 10, 'category': self.category.id})
        self.assertFalse(form.is_valid())
