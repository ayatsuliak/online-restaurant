from __future__ import absolute_import

import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'notify-undelivered-orders-every-day': {
        'task': 'orders.tasks.notify_undelivered_orders',
        'schedule': crontab(hour=9, minute=0),
    },
}
