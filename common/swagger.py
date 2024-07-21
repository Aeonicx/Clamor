from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator


class CustomSchemaGenerator(OpenAPISchemaGenerator):
    def get_endpoints(self, request):
        endpoints = super().get_endpoints(request)
        return endpoints


# main view
schema_view = get_schema_view(
    openapi.Info(
        title="Clamor API List",
        default_version="v1",
        description="This is the documentation of the APIs of Clamor.",
        contact=openapi.Contact(email="info@vyrazu.com"),
    ),
    generator_class=CustomSchemaGenerator,
    public=True,
    permission_classes=[permissions.AllowAny],
)
