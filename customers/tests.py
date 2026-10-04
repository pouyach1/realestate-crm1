from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Customer


class CustomerDeleteTests(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('admin', 'admin@example.com', 'AdminPass123!')
        self.user = User.objects.create_user('user', 'user@example.com', 'UserPass123!')
        self.customer = Customer.objects.create(
            name='علی تست',
            phone='09120000000',
            request_type='buy',
        )

    def test_delete_confirmation_renders_for_superuser(self):
        self.client.login(username='admin', password='AdminPass123!')
        response = self.client.get(reverse('customers:delete', args=[self.customer.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'حذف مشتری')
        self.assertTemplateUsed(response, 'customers/customer_confirm_delete.html')

    def test_superuser_can_delete_customer(self):
        self.client.login(username='admin', password='AdminPass123!')
        response = self.client.post(reverse('customers:delete', args=[self.customer.pk]))
        self.assertRedirects(response, reverse('customers:list'))
        self.assertFalse(Customer.objects.filter(pk=self.customer.pk).exists())

    def test_normal_user_cannot_delete_customer(self):
        self.client.login(username='user', password='UserPass123!')
        response = self.client.post(reverse('customers:delete', args=[self.customer.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Customer.objects.filter(pk=self.customer.pk).exists())

    def test_anonymous_cannot_delete_customer(self):
        response = self.client.post(reverse('customers:delete', args=[self.customer.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Customer.objects.filter(pk=self.customer.pk).exists())
