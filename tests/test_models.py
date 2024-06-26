"""Tests for models."""
from datetime import datetime, timezone

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from companies_app import models


def create_str_test(model, attrs, expected):
    """
    Create a test method for checking the string representation of a model instance.

    Args:
        model (class): The model class to test.
        attrs (dict): Dictionary containing attributes for creating the instance.
        expected (str): The expected string representation of the instance.

    Returns:
        test: A test method for checking the string representation.
    """

    def test(self):
        self.assertEqual(str(model.objects.create(**attrs)), expected)

    return test


company_attrs = {'title': 'ABC', 'phone': '+79999999999'}
equipment_attrs = {'title': 'New Equipment', 'size': 20}
review_attrs = {'text': 'New Review', 'rating': 3}
address_attrs = {'street_name': 'qwe', 'city': 'asd', 'state': 'sdf', 'house_number': 2}
category_attrs = {'title': 'New Category'}

test_str_data = (
    (models.Company, company_attrs, 'ABC: +79999999999 '),
    (models.Equipment, equipment_attrs, 'None: New Equipment, 20'),
    (models.Review, review_attrs, 'New Review: 3'),
    (models.Address, address_attrs, 'qwe'),
    (models.Category, category_attrs, 'New Category'),
)

test_str_methods = {f'test_{args[0].__name__}': create_str_test(*args) for args in test_str_data}
TestStr = type('TestStr', (TestCase,), test_str_methods)


class TestClientModel(TestCase):
    """Test case for the Client model."""

    def setUp(self):
        """Set up the test environment by creating a user and a client."""
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            email='testuser@example.com',
            password='testpassword123',
        )
        self.client = models.Client.objects.create(user=self.user)

    def test_client_str(self):
        """Test the string representation of the Client model."""
        expected_str = f'{self.user.username} {self.user.first_name} {self.user.last_name}'
        self.assertEqual(str(self.client), expected_str)

    def test_client_username_property(self):
        """Test the username property of the Client model."""
        self.assertEqual(self.client.username, self.user.username)

    def test_client_first_name_property(self):
        """Test the first name property of the Client model."""
        self.assertEqual(self.client.first_name, self.user.first_name)

    def test_client_last_name_property(self):
        """Test the last name property of the Client model."""
        self.assertEqual(self.client.last_name, self.user.last_name)

    def test_client_email_property(self):
        """Test the email property of the Client model."""
        self.assertEqual(self.client.email, self.user.email)


class TestLinks(TestCase):
    """Test case for model links."""

    def test_company_equipment(self):
        """Test the link between Company and Equipment models."""
        company = models.Company.objects.create(**company_attrs)
        equipment = models.Equipment.objects.create(**equipment_attrs)
        company.equipments.add(equipment)

        link = models.CompanyEquipment.objects.get(company=company, equipment=equipment)

        self.assertEqual(str(link), f'{company} - {equipment}')


PAST_YEAR = 2007
FUTURE_YEAR = 3000

valid_tests = (
    (models.check_created, datetime(PAST_YEAR, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc)),
    (models.check_modified, datetime(PAST_YEAR, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc)),
    (models.check_valid_phone, '+79999999999'),
)
invalid_tests = (
    (models.check_created, datetime(FUTURE_YEAR, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc)),
    (models.check_modified, datetime(FUTURE_YEAR, 1, 1, 1, 1, 1, 1, tzinfo=timezone.utc)),
    (models.check_valid_phone, '+999'),
)


def create_validation_test(validator, validation_value, valid=True):
    """
    Create a validation test method for a specific validator.

    Args:
        validator (function): The validation function to test.
        validation_value: The value to be validated.
        valid (bool, optional): Flag indicating whether the value is expected to be valid or not.

    Returns:
        test: A test method for the validation function.
    """
    if valid:
        return lambda _: validator(validation_value)

    def test(self):
        with self.assertRaises(ValidationError):
            validator(validation_value)

    return test


valid_methods = {
    f'test_valid_{args[0].__name__}': create_validation_test(*args) for args in valid_tests
}
invalid_methods = {
    f'test_invalid_{args[0].__name__}': create_validation_test(*args, valid=False) for args in
    invalid_tests
}

TestValidators = type('TestValidators', (TestCase,), valid_methods | invalid_methods)
