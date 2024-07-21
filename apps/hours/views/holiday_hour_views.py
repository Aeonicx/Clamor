from apps.restaurant.models import Restaurant
from apps.hours.models import HolidayHour
from apps.hours.serializers import HolidayHourSerializer
from rest_framework.views import APIView
from django.http import Http404
from common.utils import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from common.permissions import UserBasedPermission


class HolidayHourList(APIView):
    """
    create a new holiday-hour.
    """

    permission_classes = [UserBasedPermission]

    @swagger_auto_schema(request_body=HolidayHourSerializer)
    def post(self, request, format=None):
        serializer = HolidayHourSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            restaurant = request.data.get("restaurant")
            obj = Restaurant.objects.get(pk=restaurant)
            self.check_object_permissions(self.request, obj)
            serializer.save(created_by=request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class HolidayHourDetail(APIView):
    """
    Retrieve, update or delete a holiday-hour instance.
    """

    permission_classes = [UserBasedPermission]

    def get_object(self, pk):
        try:
            obj = HolidayHour.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj.restaurant)
            return obj
        except HolidayHour.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        holiday_hour = self.get_object(pk)
        serializer = HolidayHourSerializer(holiday_hour)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=HolidayHourSerializer)
    def patch(self, request, pk, format=None):
        holiday_hour = self.get_object(pk)
        serializer = HolidayHourSerializer(
            holiday_hour, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save(updated_by=request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        holiday_hour = self.get_object(pk)
        holiday_hour.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
