from apps.restaurant.models import Restaurant
from apps.setup.models import BankDetails
from django.http import Http404
from rest_framework.views import APIView
from common.utils import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from apps.setup.serializers import BankDetailsSerializer
from common.permissions import UserBasedPermission


class BankDetailsList(APIView):
    """
    create a new bank-details.
    """

    permission_classes = [UserBasedPermission]

    @swagger_auto_schema(request_body=BankDetailsSerializer)
    def post(self, request, format=None):
        serializer = BankDetailsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            restaurant = request.data.get("restaurant")
            obj = Restaurant.objects.get(pk=restaurant)
            self.check_object_permissions(self.request, obj)
            bank_details = serializer.save(created_by=request.user)
            serializer = BankDetailsSerializer(bank_details)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class BankDetailsDetail(APIView):
    """
    Retrieve or update a bank-details instance.
    """

    permission_classes = [UserBasedPermission]

    def get_object(self, pk):
        try:
            obj = BankDetails.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj.restaurant)
            return obj
        except BankDetails.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        bank_details = self.get_object(pk)
        serializer = BankDetailsSerializer(bank_details)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=BankDetailsSerializer)
    def patch(self, request, pk, format=None):
        bank_details = self.get_object(pk)
        serializer = BankDetailsSerializer(
            bank_details, data=request.data, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            bank_details = serializer.save(updated_by=request.user)
            serializer = BankDetailsSerializer(bank_details)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
