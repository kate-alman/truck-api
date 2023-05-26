# Generated by Django 4.1.6 on 2023-05-24 13:48
import pandas as pd

from django.db import migrations


def get_locations(apps, schema_editor):
    LocationMap = apps.get_model("truck_app", "LocationMap")
    df = pd.read_csv("truck_app/migrations/uszips.csv", sep=",")
    data = df.iterrows()
    bulk_list = []
    for index, row in data:
        zip = row["zip"]
        city = row["city"]
        state = row["state_name"]
        latitude = row["lat"]
        longitude = row["lng"]
        bulk_list.append(
            LocationMap(
                zip=zip, city=city, state=state, latitude=latitude, longitude=longitude
            )
        )
    LocationMap.objects.bulk_create(bulk_list)


class Migration(migrations.Migration):
    dependencies = [
        ("truck_app", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(get_locations),
    ]
