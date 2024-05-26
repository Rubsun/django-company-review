from django.contrib.messages import get_messages
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from companies_app.models import Company, Equipment, Review, Client, Address, Category
from companies_app.forms import RegistrationForm, ReviewForm, CompanyForm, EquipmentForm

class ViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='12345',
            email='test@example.com'
        )
        self.client.force_login(self.user)
        self.client_instance = Client.objects.create(user=self.user)

    def test_company_creation(self):

        company_data = {
            'title': 'Test Company',
            'client_id': self.client_instance.id,
            'phone': '123-456-7890'
        }

        response = self.client.post(reverse('create_company'), company_data)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Company.objects.filter(title='Test Company').exists())

    def test_create_equipment(self):
        category = Category.objects.create(title='Test Category')
        equipment_data = {
            'title': 'New Equipment',
            'size': 20,
            'category': category.id,
        }
        response = self.client.post(reverse('create_equipment'), data=equipment_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Equipment.objects.filter(title='New Equipment', size=20).exists())

    def test_add_equipment_to_company(self):
        category = Category.objects.create(title='Test Category')
        equipment = Equipment.objects.create(title='Test Equipment', size=10, category=category, client=self.client_instance)
        address = Address.objects.create(street_name='Test Street', city='Test City', state='Test State', house_number=123)
        company = Company.objects.create(title='Test Company', phone='+1234567890', address=address, client=self.client_instance)
        response = self.client.post(reverse('add_equipment_to_company', args=[equipment.id]), {'company_id': company.id})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Company.objects.filter(equipments=equipment, id=company.id).exists())

    def test_delete_review(self):
        category = Category.objects.create(title='Test Category')
        equipment = Equipment.objects.create(title='Test Equipment', size=10, category=category, client=self.client_instance)
        review = Review.objects.create(text='Test Review', rating=5, client=self.client_instance, equipment=equipment)
        response = self.client.post(reverse('delete_review', args=[review.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(id=review.id).exists())

    def test_delete_equipment(self):
        category = Category.objects.create(title='Test Category')
        equipment = Equipment.objects.create(title='Test Equipment', size=10, category=category, client=self.client_instance)
        review = Review.objects.create(text='Test Review', rating=5, client=self.client_instance, equipment=equipment)
        response = self.client.post(reverse('delete_review', args=[review.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(id=review.id).exists())


    def test_delete_equipment_no_permission(self):
        category = Category.objects.create(title='Test Category')
        other_user = User.objects.create_user(username='otheruser', password='password')
        other_client = Client.objects.create(user=other_user)
        equipment = Equipment.objects.create(title='Other Equipment', size=15, category=category, client=other_client)

        response = self.client.post(reverse('delete_equipment', args=[equipment.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Equipment.objects.filter(id=equipment.id).exists())

