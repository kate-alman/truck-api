from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from truck_app.models import Goods, Truck
from truck_app.serializers import (
    GoodsListSerializer,
    GoodsUpdateSerializer,
    TruckSerializer,
)


class APIListPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 10000


@method_decorator(
    name="get", decorator=swagger_auto_schema(operation_description="Get list of goods")
)
@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        operation_description="Add new goods"
    ),
)
class GoodsAPIList(generics.ListCreateAPIView):
    queryset = Goods.objects.select_related("pick_up", "deliver").all()
    serializer_class = GoodsListSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, )
    pagination_class = APIListPagination

    def filter_queryset(self, queryset):
        weight = self.request.GET.get("weight")
        if weight:
            return Goods.objects.select_related("pick_up", "delivery").filter(
                weight__lte=weight
            )
        return Goods.objects.select_related("pick_up", "delivery").all()


@method_decorator(
    name="get", decorator=swagger_auto_schema(operation_description="Get goods by id")
)
@method_decorator(
    name="put",
    decorator=swagger_auto_schema(
        operation_description="Change weight and/or description of goods by id"
    ),
)
@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        operation_description="Change weight and/or description of goods by id"
    ),
)
@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(operation_description="Delete goods by id"),
)
class GoodsIdAPIList(generics.RetrieveUpdateDestroyAPIView):
    queryset = Goods.objects.select_related("pick_up", "delivery").all()
    serializer_class = GoodsUpdateSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, )


@method_decorator(
    name="get", decorator=swagger_auto_schema(operation_description="Get truck by id")
)
@method_decorator(
    name="put",
    decorator=swagger_auto_schema(
        operation_description="Change number, zip (current location), capacity of truck by id"
    ),
)
@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        operation_description="Change number, zip (current location), capacity of truck by id"
    ),
)
class TruckAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Truck.objects.select_related("current_location").all()
    serializer_class = TruckSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, )
