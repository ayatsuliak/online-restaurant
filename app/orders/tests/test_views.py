from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from menu.models import MenuItem
from orders.models import Order

User = get_user_model()


class OrderViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='viewuser',
                                             password='pass')
        self.menu_item = MenuItem.objects.create(name='Sushi', price=80)

    def test_requires_login(self):
        response = self.client.get(reverse('orders:create_order'))
        self.assertEqual(response.status_code, 302)

    def test_successful_order_creation(self):
        self.client.login(username='viewuser', password='pass')
        future_time = (timezone.localtime(timezone.now())
                       + timedelta(minutes=40))
        response = self.client.post(reverse('orders:create_order'), {
            'items': [str(self.menu_item.pk)],
            'scheduled_time': future_time.strftime('%Y-%m-%dT%H:%M')
        })
        self.assertRedirects(response, reverse('menu:menu_list'))
        self.assertEqual(Order.objects.count(), 1)

    def test_order_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('orders:create_order'))
        self.assertRedirects(response,
                             f"/auth/login/?next={reverse('orders:create_order')}")
