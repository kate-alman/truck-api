# Generated by Django 4.1.6 on 2023-05-25 06:39
import random
import string

from django.db import migrations

from truck_app.models import LocationMap


def set_start_trucks(apps, schema_editor):
    Truck = apps.get_model("truck_app", "Truck")
    start = 1000
    locations = LocationMap.objects.all()
    for num in range(1, 21):
        character = random.choice(string.ascii_uppercase)
        start += 1
        number = f"{start}{character}"
        current_location = locations[num]
        capacity = random.randrange(1, 1000)
        Truck.objects.create(
            number=number, current_location_id=current_location.pk, capacity=capacity
        )


class Migration(migrations.Migration):
    dependencies = [
        ("truck_app", "0002_auto_20230525_0938"),
    ]

    operations = [
        migrations.RunPython(set_start_trucks),
    ]
