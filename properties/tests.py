from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Favorite, Property


class PropertyDetailAccessTests(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser('admin', 'admin@example.com', 'AdminPass123!')
        self.user = User.objects.create_user('user', 'user@example.com', 'UserPass123!')
        self.property = Property.objects.create(
            title='ویلای تست',
            property_type='villa',
            price=750000000,
            area=120,
            address='تهران',
            status='available',
        )

    def test_guest_can_view_property_detail_with_display_price(self):
        response = self.client.get(reverse('properties:detail', args=[self.property.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '۵۰۰ - ۱ میلیارد')
        self.assertContains(response, 'وارد شوید')
        self.assertNotContains(response, 'ویرایش')
        self.assertNotContains(response, 'حذف')

    def test_authenticated_user_sees_exact_price_without_edit_controls(self):
        self.client.login(username='user', password='UserPass123!')
        response = self.client.get(reverse('properties:detail', args=[self.property.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'میلیون تومان')
        self.assertNotContains(response, 'ویرایش')
        self.assertNotContains(response, 'حذف')

    def test_superuser_sees_edit_delete_controls(self):
        self.client.login(username='admin', password='AdminPass123!')
        response = self.client.get(reverse('properties:detail', args=[self.property.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'ویرایش')
        self.assertContains(response, 'حذف')

    def test_normal_user_cannot_edit_or_delete(self):
        self.client.login(username='user', password='UserPass123!')
        edit_response = self.client.get(reverse('properties:update', args=[self.property.pk]))
        delete_response = self.client.get(reverse('properties:delete', args=[self.property.pk]))
        self.assertEqual(edit_response.status_code, 302)
        self.assertEqual(delete_response.status_code, 302)

    def test_view_count_increments(self):
        before = self.property.view_count
        self.client.get(reverse('properties:detail', args=[self.property.pk]))
        self.property.refresh_from_db()
        self.assertEqual(self.property.view_count, before + 1)


class FavoriteToggleTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@example.com', 'UserPass123!')
        self.property = Property.objects.create(
            title='آپارتمان تست',
            property_type='apartment',
            price=1000000000,
            area=90,
            address='اصفهان',
            status='available',
        )

    def test_toggle_favorite_add_and_remove(self):
        self.client.login(username='user', password='UserPass123!')
        url = reverse('properties:toggle_favorite')

        add_response = self.client.post(url, {'property_id': self.property.pk})
        self.assertEqual(add_response.status_code, 200)
        self.assertEqual(add_response.json()['status'], 'added')
        self.assertTrue(Favorite.objects.filter(user=self.user, property=self.property).exists())

        remove_response = self.client.post(url, {'property_id': self.property.pk})
        self.assertEqual(remove_response.status_code, 200)
        self.assertEqual(remove_response.json()['status'], 'removed')
        self.assertFalse(Favorite.objects.filter(user=self.user, property=self.property).exists())

    def test_invalid_property_id_returns_404(self):
        self.client.login(username='user', password='UserPass123!')
        response = self.client.post(reverse('properties:toggle_favorite'), {'property_id': 999999})
        self.assertEqual(response.status_code, 404)

    def test_favorites_queryset_uses_select_related(self):
        Favorite.objects.create(user=self.user, property=self.property)
        self.client.login(username='user', password='UserPass123!')
        response = self.client.get(reverse('properties:favorites'))
        self.assertEqual(response.status_code, 200)
        qs = response.context['favorites']
        self.assertIn('property', qs.query.select_related)
