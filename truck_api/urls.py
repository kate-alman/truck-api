"""
URL configuration for truck_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.defaults import page_not_found
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from truck_api import settings
from truck_app.swagger_generator import CustomOpenAPISchemaGenerator

schema_view = get_schema_view(
    openapi.Info(
        title="Truck API",
        default_version="v1",
        description="Description of the available service methods for finding the nearest vehicles to the cargo.",
        contact=openapi.Contact(email="ekaterina.aman@syandex.ru"),
    ),
    public=True,
    permission_classes=[IsAuthenticatedOrReadOnly, ],
    generator_class=CustomOpenAPISchemaGenerator,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("truck_app.urls")),
    re_path(
        r"swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found
