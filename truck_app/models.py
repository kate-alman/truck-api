import re

from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from geopy import distance


def validate_truck_number(value):
    """ Проверяет соответствие номера заданному шаблону """
    reg = re.compile(r"^[1-9]{1}[\d]{3}[A-Z]{1}$")
    if not reg.match(value):
        raise ValidationError("%s number does not comply" % value)


def validate_zip(value):
    """ Проверяет наличие адреса по zip-коду в базе """
    try:
        LocationMap.objects.get(zip=value)
    except ObjectDoesNotExist:
        raise ValidationError("Location with this zip does not exist, please contact the administrator")


class LocationMap(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.IntegerField(primary_key=True)
    latitude = models.DecimalField(max_digits=22, decimal_places=5)
    longitude = models.DecimalField(max_digits=22, decimal_places=5)

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):
        return f"City {self.city}; State {self.state}; zip {self.zip}"


class Truck(models.Model):
    number = models.CharField(
        max_length=5, unique=True, validators=[validate_truck_number]
    )
    current_location = models.ForeignKey(
        LocationMap,
        null=True,
        on_delete=models.SET_NULL,
        related_name="current_location",
    )
    capacity = models.IntegerField(
        validators=[MaxValueValidator(1000), MinValueValidator(1)]
    )

    class Meta:
        verbose_name_plural = "Trucks"

    def __str__(self):
        return f"Truck {self.number}; capacity {self.capacity}"


class Goods(models.Model):
    pick_up = models.ForeignKey(
        LocationMap, null=True, on_delete=models.SET_NULL, related_name="from_pick_up"
    )
    delivery = models.ForeignKey(
        LocationMap, null=True, on_delete=models.SET_NULL, related_name="to_delivery"
    )
    distance = models.FloatField()
    weight = models.IntegerField(
        validators=[MaxValueValidator(1000), MinValueValidator(1)]
    )
    description = models.CharField(max_length=500)
    photo = models.ImageField(
        upload_to="cargo_photos/%Y/%m/%d/",
        blank=True,
    )

    class Meta:
        verbose_name_plural = "Goods"

    def __str__(self):
        return f"From {self.pick_up} to {self.delivery} (distance {self.distance}"

    def save(self, *args, **kwargs):
        """ При создании груза дополнительно рассчитывает и сохраняет расстояние (в милях)"""
        self.distance = calc_distance(self.pick_up, self.delivery)
        super().save(*args, **kwargs)


def calc_distance(start_coord: LocationMap, dest_coord: LocationMap) -> int:
    """ Расчет расстояния по координатам от стартовой до конечной точки (в милях) """
    coords_start = (round(start_coord.latitude, 5), round(start_coord.longitude, 5))
    coords_dest = (round(dest_coord.latitude, 5), round(dest_coord.longitude, 5))
    distance_geopy = distance.distance(coords_start, coords_dest).miles
    return distance_geopy


