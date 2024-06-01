"""Tests for CRUD."""
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from companies_app.models import (Address, Category, Client, Company,
                                  Equipment, Review)


class ViewTests(TestCase):
    """Test case for views."""

    def setUp(self):
        """Set up the test environment by creating a user and logging them in."""
        self.user = User.objects.create_user(
            username='testuser',
            password='12345',
            email='test@example.com',
        )
        self.client.force_login(self.user)
        self.client_instance = Client.objects.create(user=self.user)

    def test_company_creation(self):
        """Test company creation view."""
        company_data = {
            'title': 'Test Company',
            'phone': '+79282037102',
            'street_name': 'Test Street',
            'city': 'Test City',
            'state': 'Test State',
            'house_number': '123',
        }

        response = self.client.post(reverse('create_company'), company_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Company.objects.filter(title='Test Company').exists())

    def test_create_equipment(self):
        """Test create equipment view."""
        category = Category.objects.create(title='Test Category1')
        equipment_data = {
            'title': 'New Equipment',
            'size': 20,
            'category': category.id,
        }
        response = self.client.post(reverse('create_equipment'), data=equipment_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Equipment.objects.filter(title='New Equipment', size=20).exists())

    def test_add_equipment_to_company(self):
        """Test add equipment to company view."""
        category = Category.objects.create(title='Test Category2')
        equipment = Equipment.objects.create(
            title='Test Equipment', size=10, category=category, client=self.client_instance,
        )
        address = Address.objects.create(
            street_name='Test Street', city='Test City', state='Test State', house_number=123,
        )
        company = Company.objects.create(
            title='TestCompany', phone='+1234567890', address=address, client=self.client_instance,
        )
        response = self.client.post(
            reverse('add_equipment_to_company', args=[equipment.id]), {'company_id': company.id},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Company.objects.filter(equipments=equipment, id=company.id).exists())

    def test_delete_review(self):
        """Test delete review view."""
        category = Category.objects.create(title='Test Category3')
        equipment = Equipment.objects.create(
            title='Test Equipment', size=10, category=category, client=self.client_instance,
        )
        review = Review.objects.create(
            text='Test Review', rating=5, client=self.client_instance, equipment=equipment,
        )
        response = self.client.post(reverse('delete_review', args=[review.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(id=review.id).exists())

    def test_delete_equipment(self):
        """Test delete equipment view."""
        category = Category.objects.create(title='Test Category')
        equipment = Equipment.objects.create(
            title='Test Equipment', size=10, category=category, client=self.client_instance,
        )
        review = Review.objects.create(
            text='Test Review', rating=5, client=self.client_instance, equipment=equipment,
        )
        response = self.client.post(reverse('delete_equipment', args=[equipment.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(id=review.id).exists())

    def test_delete_equipment_no_permission(self):
        """Test delete equipment view without permission."""
        category = Category.objects.create(title='Test Category')
        other_user = User.objects.create_user(username='otheruser', password='password')
        other_client = Client.objects.create(user=other_user)
        equipment = Equipment.objects.create(
            title='Other Equipment', size=15, category=category, client=other_client,
        )

        response = self.client.post(reverse('delete_equipment', args=[equipment.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Equipment.objects.filter(id=equipment.id).exists())
