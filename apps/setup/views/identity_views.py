from apps.restaurant.models import Restaurant
from apps.setup.models import Identity
from django.http import Http404
from rest_framework.views import APIView
from common.utils import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from apps.setup.serializers import IdentitySerializer
from common.permissions import UserBasedPermission


class IdentityList(APIView):
    """
    create a new identity.
    """

    permission_classes = [UserBasedPermission]

    @swagger_auto_schema(request_body=IdentitySerializer)
    def post(self, request, format=None):
        serializer = IdentitySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            restaurant = request.data.get("restaurant")
            obj = Restaurant.objects.get(pk=restaurant)
            self.check_object_permissions(self.request, obj)
            identity = serializer.save(created_by=request.user)
            serializer = IdentitySerializer(identity)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class IdentityDetail(APIView):
    """
    Retrieve or update a identity instance.
    """

    permission_classes = [UserBasedPermission]

    def get_object(self, pk):
        try:
            obj = Identity.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj.restaurant)
            return obj
        except Identity.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        identity = self.get_object(pk)
        serializer = IdentitySerializer(identity)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=IdentitySerializer)
    def patch(self, request, pk, format=None):
        identity = self.get_object(pk)
        serializer = IdentitySerializer(identity, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            identity = serializer.save(updated_by=request.user)
            serializer = IdentitySerializer(identity)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
