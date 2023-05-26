from celery import shared_task

from truck_app.models import Truck, LocationMap


@shared_task(name="update_locations")
def update_locations(message, *args, **kwargs):
    location = LocationMap.objects.order_by("?").first()
    Truck.objects.all().update(current_location=location)
    print(f"{message}")
