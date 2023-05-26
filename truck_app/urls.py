from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenVerifyView,
    TokenRefreshView,
)

from truck_app.views import GoodsAPIList, GoodsIdAPIList, TruckAPIUpdate

urlpatterns = [
    path("v1/goods/", GoodsAPIList.as_view(), name="goods"),
    path("v1/goods/<int:pk>/", GoodsIdAPIList.as_view(), name="goods_info"),
    path("v1/truck/<int:pk>/", TruckAPIUpdate.as_view(), name="truck"),
    path("v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("v1/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
