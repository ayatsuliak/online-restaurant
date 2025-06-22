from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from menu.models import MenuItem
from orders.forms import OrderForm

User = get_user_model()


class OrderFormTests(TestCase):
    def setUp(self):
        self.menu_item = MenuItem.objects.create(name='Pizza', price=100)

    def test_valid_order(self):
        future_time = (timezone.localtime(timezone.now())
                       + timedelta(minutes=45))
        form = OrderForm(data={
            'items': [str(self.menu_item.pk)],
            'scheduled_time': future_time.strftime('%Y-%m-%dT%H:%M')
        })
        self.assertTrue(form.is_valid())

    def test_order_in_past_invalid(self):
        past_time = timezone.localtime(timezone.now()) - timedelta(minutes=10)
        form = OrderForm(data={
            'items': [str(self.menu_item.pk)],
            'scheduled_time': past_time.strftime('%Y-%m-%dT%H:%M')
        })
        self.assertFalse(form.is_valid())
        self.assertIn('scheduled_time', form.errors)

    def test_order_less_than_30_minutes_invalid(self):
        short_time = timezone.localtime(timezone.now()) + timedelta(minutes=10)
        form = OrderForm(data={
            'items': [str(self.menu_item.pk)],
            'scheduled_time': short_time.strftime('%Y-%m-%dT%H:%M')
        })
        self.assertFalse(form.is_valid())
        self.assertIn('scheduled_time', form.errors)

    def test_missing_items_field_invalid(self):
        future_time = (timezone.localtime(timezone.now())
                       + timedelta(minutes=40))
        form = OrderForm(data={
            'scheduled_time': future_time.strftime('%Y-%m-%dT%H:%M')
        })
        self.assertFalse(form.is_valid())
        self.assertIn('items', form.errors)

    def test_missing_scheduled_time_invalid(self):
        form = OrderForm(data={
            'items': [str(self.menu_item.pk)]
        })
        self.assertFalse(form.is_valid())
        self.assertIn('scheduled_time', form.errors)
