from rest_framework import serializers

from truck_app.models import (
    Goods,
    LocationMap,
    Truck,
    calc_distance,
    validate_truck_number, validate_zip,
)


class LocationMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationMap
        fields = ("zip", "city", "state")
        read_only_fields = ("city", "state")
        extra_kwargs = {
            "zip": {"validators": [validate_zip]},
        }


class TruckSerializer(serializers.ModelSerializer):
    current_location = LocationMapSerializer()
    distance_to_pick_up = serializers.SerializerMethodField("set_distance")

    class Meta:
        model = Truck
        fields = (
            "number",
            "capacity",
            "current_location",
            "distance_to_pick_up",
        )
        extra_kwargs = {
            "number": {"validators": [validate_truck_number]},
        }

    def update(self, instance, validated_data):
        location_data = validated_data.pop("current_location")
        current_location = LocationMap.objects.get(**location_data)
        validated_data["current_location"] = current_location
        return super().update(instance, validated_data)

    @staticmethod
    def set_distance(obj):
        """ Рассчитывает расстояние от машины до точки погрузки """
        try:
            distance_to_pick_up = obj.get("distance_to_pick_up", None)
            return int(distance_to_pick_up)
        except AttributeError:
            return


class GoodsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        self.trucks = Truck.objects.select_related("current_location").all()
        super().__init__(*args, **kwargs)


class GoodsListSerializer(GoodsSerializer):
    pick_up = LocationMapSerializer()
    delivery = LocationMapSerializer()
    distance = serializers.IntegerField(read_only=True)
    description = serializers.CharField(max_length=500)
    weight = serializers.IntegerField(min_value=1, max_value=1000)
    photo = serializers.ImageField(required=False)
    nearby_trucks = serializers.SerializerMethodField(method_name="get_nearby_trucks")

    class Meta:
        model = Goods
        fields = "__all__"

    def create(self, validated_data):
        pick_data = validated_data.pop("pick_up")
        pick_up = LocationMap.objects.get(**pick_data)
        delivery_data = validated_data.pop("delivery")
        delivery = LocationMap.objects.get(**delivery_data)
        instance = Goods.objects.create(
            pick_up_id=pick_up.zip, delivery_id=delivery.zip, **validated_data
        )
        return instance

    def get_nearby_trucks(self, obj: Goods, max_distance: int = 450) -> int:
        """
        Возвращает количество ближайших машин на заданном расстоянии
        :param obj: данные о грузе
        :param max_distance: расстояние от погрузки до машины, по умолчанию 450 миль
        """
        max_distance = self.context.get("request").GET.get("max_distance", max_distance)
        goods_location = obj.pick_up
        nearby = [
            TruckSerializer(truck).data
            for truck in self.trucks
            if calc_distance(goods_location, truck.current_location)
            <= int(max_distance)
        ]
        return len(nearby)


class GoodsUpdateSerializer(GoodsSerializer):
    trucks_around = serializers.SerializerMethodField("get_trucks")

    class Meta:
        model = Goods
        fields = ("pick_up", "delivery", "weight", "description", "trucks_around")
        read_only_fields = ("pick_up", "delivery", "distance")

    def get_trucks(self, obj: Goods, max_distance: float = float("inf"), capacity: float = float("inf")) -> list:
        """
        Возвращает машины и их расстояние до груза
        :param obj: данные о грузе
        :param max_distance: на каком расстоянии от погрузки выдавать машины, по умолчанию бесконечность
        :param capacity: с какой грузоподъемностью выдавать машины, по умолчанию бесконечность
        """
        max_distance = self.context.get("request").GET.get("max_distance", max_distance)
        capacity = self.context.get("request").GET.get("capacity", capacity)
        goods_location = obj.pick_up
        all_trucks = [
            TruckSerializer(
                {
                    "number": truck.number,
                    "current_location": truck.current_location,
                    "distance_to_pick_up": calc_distance(
                        goods_location, truck.current_location
                    ),
                    "capacity": truck.capacity,
                }
            ).data
            for truck in self.trucks
            if truck.capacity <= float(capacity)
        ]
        all_trucks = list(
            filter(
                lambda x: x["distance_to_pick_up"] <= float(max_distance), all_trucks
            )
        )
        return all_trucks
