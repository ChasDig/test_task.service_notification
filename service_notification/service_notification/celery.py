import os
from celery import Celery


os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "service_notification.settings",
)

app = Celery("service_notification")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
