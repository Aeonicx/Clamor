from apps.restaurant.models import Restaurant
from apps.setup.models import Availability
from django.http import Http404
from rest_framework.views import APIView
from common.utils import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from common.permissions import UserBasedPermission
from apps.setup.serializers import (
    AvailabilityReadSerializer,
    AvailabilityWriteSerializer,
)


class AvailabilityList(APIView):
    """
    create a new availability.
    """

    permission_classes = [UserBasedPermission]

    @swagger_auto_schema(request_body=AvailabilityWriteSerializer)
    def post(self, request, format=None):
        serializer = AvailabilityWriteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            restaurant = request.data.get("restaurant")
            obj = Restaurant.objects.get(pk=restaurant)
            self.check_object_permissions(self.request, obj)
            availability = serializer.save(created_by=request.user)
            serializer = AvailabilityReadSerializer(availability)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class AvailabilityDetail(APIView):
    """
    Retrieve or update a availability instance.
    """

    permission_classes = [UserBasedPermission]

    def get_object(self, pk):
        try:
            obj = Availability.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj.restaurant)
            return obj
        except Availability.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        availability = self.get_object(pk)
        serializer = AvailabilityReadSerializer(availability)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=AvailabilityWriteSerializer)
    def patch(self, request, pk, format=None):
        availability = self.get_object(pk)
        serializer = AvailabilityWriteSerializer(
            availability, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            availability = serializer.save(updated_by=request.user)
            serializer = AvailabilityReadSerializer(availability)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
