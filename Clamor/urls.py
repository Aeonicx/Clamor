from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from common.swagger import schema_view

API_ROOT = "api/"


urlpatterns = [
    path("admin/", admin.site.urls),
    # apis for authentication
    path(API_ROOT + "auth/", include("authentication.urls")),
    # apis for collection
    path(API_ROOT, include("collection.urls")),
    # apis for restaurant
    path(API_ROOT, include("apps.restaurant.urls")),
    # apis for setup
    path(API_ROOT, include("apps.setup.urls")),
    # apis for hours
    path(API_ROOT, include("apps.hours.urls")),
    # apis for category
    path(API_ROOT, include("apps.category.urls")),
]


if settings.SWAGGER:
    urlpatterns += (path("", schema_view.with_ui("swagger", cache_timeout=0)),)

if settings.DEBUG:  # development
    # serving media
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
