from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .models import Order


@shared_task
def send_order_confirmation_email(user_email, order_id):
    subject = f"Your Order #{order_id} has been received"
    message = "Thank you for your order! We will deliver it soon."
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )


@shared_task
def notify_undelivered_orders():
    now = timezone.now()
    orders = Order.objects.filter(delivered=False)

    for order in orders:
        scheduled = order.scheduled_time

        if timezone.is_naive(scheduled):
            scheduled = timezone.make_aware(scheduled,
                                            timezone.get_current_timezone())

        if scheduled <= now:
            order.delivered = True
            order.save()

            send_mail(
                subject="Your order has been delivered",
                message=f"Order #{order.id} "
                        f"has been marked as delivered. Enjoy your meal!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[order.user.email],
                fail_silently=False
            )
