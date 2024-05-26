from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from companies_app.forms import RegistrationForm, LoginForm, ReviewForm, CompanyForm, EquipmentForm
from companies_app.models import Client, Equipment, Category


class RegistrationFormTest(TestCase):
    _valid_data = {
        'username': 'username',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'email': 'email@email.com',
        'password1': 'Azpm1029!',
        'password2': 'Azpm1029!',
    }

    def test_valid(self):
        self.assertTrue(RegistrationForm(data=self._valid_data).is_valid())

    def invalid(self, invalid_data):
        data = self._valid_data.copy()
        for field, value in invalid_data:
            data[field] = value
        self.assertFalse(RegistrationForm(data=data).is_valid())

    def test_short_password(self):
        self.invalid(
            (
                ('password1', 'abc'),
                ('password2', 'abc'),
            )
        )

    def test_common_password(self):
        self.invalid(
            (
                ('password1', 'abcdef123'),
                ('password2', 'abcdef123'),
            )
        )

    def test_different_passwords(self):
        self.invalid(
            (
                ('password1', 'ASDksdjn9734'),
                ('password2', 'LKKJdfnalnd234329'),
            )
        )

    def test_invalid_email(self):
        self.invalid(
            (
                ('email', 'abc'),
            )
        )

    def test_existing_user(self):
        username, password = 'username', 'password'
        User.objects.create(username=username, password=password)
        self.invalid(
            (
                ('username', username),
                ('password', password),
            )
        )

class LoginFormTest(TestCase):
    def test_valid(self):
        User.objects.create_user(username='testuser', password='password')
        form = LoginForm(data={'username': 'testuser', 'password': 'password'})
        self.assertTrue(form.is_valid())

    def test_invalid(self):
        form = LoginForm(data={'username': '', 'password': 'wrongpassword'})
        self.assertFalse(form.is_valid())


class ReviewFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client_model = Client.objects.create(user=self.user)
        self.equipment = Equipment.objects.create(title='Test Equipment', client=self.client_model, category=Category.objects.create(title="Test Category"))

    def test_valid(self):
        form = ReviewForm(data={'text': 'Great equipment!', 'rating': 5, 'client': self.client_model, 'equipment': self.equipment})
        self.assertTrue(form.is_valid())

    def test_invalid(self):
        form = ReviewForm(data={'text': '', 'rating': 5, 'client': self.client_model, 'equipment': self.equipment})
        self.assertFalse(form.is_valid())
class CompanyFormTest(TestCase):
    def test_valid(self):
        form = CompanyForm(data={'title': 'Test Company', 'phone': '1234567890'})
        self.assertTrue(form.is_valid())

    def test_invalid(self):
        form = CompanyForm(data={'title': '', 'phone': '1234567890'})
        self.assertFalse(form.is_valid())

class EquipmentFormTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(title='Test Category')

    def test_valid(self):
        form = EquipmentForm(data={'title': 'Test Equipment', 'size': 10, 'category': self.category.id})
        self.assertTrue(form.is_valid())

    def test_invalid(self):
        form = EquipmentForm(data={'title': '', 'size': 10, 'category': self.category.id})
        self.assertFalse(form.is_valid())


