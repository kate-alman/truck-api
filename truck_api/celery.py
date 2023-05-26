import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "truck_api.settings")

app = Celery("truck_api")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "update-location-180-seconds": {
        "task": "update_locations",
        "schedule": 180.0,
        "args": ("Locations updated!",)
    },
}
