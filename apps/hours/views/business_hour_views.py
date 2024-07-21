from apps.restaurant.models import Restaurant
from apps.hours.models import BusinessHour
from apps.hours.serializers import BusinessHourSerializer
from rest_framework.views import APIView
from django.http import Http404
from common.utils import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from common.permissions import UserBasedPermission


class BusinessHourList(APIView):
    """
    create a new business-hour.
    """

    permission_classes = [UserBasedPermission]

    @swagger_auto_schema(request_body=BusinessHourSerializer)
    def post(self, request, format=None):
        serializer = BusinessHourSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            restaurant = request.data.get("restaurant")
            obj = Restaurant.objects.get(pk=restaurant)
            self.check_object_permissions(self.request, obj)
            serializer.save(created_by=request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class BusinessHourDetail(APIView):
    """
    Retrieve, update or delete a business-hour instance.
    """

    permission_classes = [UserBasedPermission]

    def get_object(self, pk):
        try:
            obj = BusinessHour.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj.restaurant)
            return obj
        except BusinessHour.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        business_hour = self.get_object(pk)
        serializer = BusinessHourSerializer(business_hour)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=BusinessHourSerializer)
    def patch(self, request, pk, format=None):
        business_hour = self.get_object(pk)
        serializer = BusinessHourSerializer(
            business_hour, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save(updated_by=request.user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        business_hour = self.get_object(pk)
        business_hour.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
