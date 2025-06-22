from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from orders.models import Order
from orders.tasks import notify_undelivered_orders, send_order_confirmation_email

User = get_user_model()


class TaskTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u', email='u@test.com')
        self.order = Order.objects.create(
            user=self.user,
            scheduled_time=timezone.now() - timedelta(minutes=5),
            delivered=False
        )

    @patch('orders.tasks.send_mail')
    def test_send_order_confirmation(self, mock_send):
        send_order_confirmation_email(self.user.email, self.order.id)
        mock_send.assert_called_once()

    @patch('orders.tasks.send_mail')
    def test_notify_undelivered(self, mock_send):
        notify_undelivered_orders()
        mock_send.assert_called_once()
