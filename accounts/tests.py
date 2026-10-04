from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .views import PersianUserCreationForm


class RegistrationValidationTests(TestCase):
    def test_password_mismatch_fails(self):
        form = PersianUserCreationForm(data={
            'username': 'newuser',
            'password1': 'ComplexPass123!',
            'password2': 'DifferentPass123!',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_django_password_validators_reject_common_password(self):
        form = PersianUserCreationForm(data={
            'username': 'newuser',
            'password1': 'password',
            'password2': 'password',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_django_password_validators_reject_too_short(self):
        form = PersianUserCreationForm(data={
            'username': 'newuser',
            'password1': 'Ab1!',
            'password2': 'Ab1!',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_valid_registration_creates_user(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'validuser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        })
        self.assertRedirects(response, reverse('accounts:login'))
        self.assertTrue(User.objects.filter(username='validuser').exists())
