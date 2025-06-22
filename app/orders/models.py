from django.conf import settings
from django.db import models

from menu.models import MenuItem


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(MenuItem)
    scheduled_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
