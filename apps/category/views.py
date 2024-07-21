from apps.restaurant.models import Restaurant
from .models import Category
from .serializers import CategoryReadSerializer, CategoryWriteSerializer
from django.http import Http404
from rest_framework.views import APIView
from common.utils import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from common.permissions import UserBasedPermission
from .utils import reorder_catagories


class CategoryList(APIView):
    """
    List all categories, or create a new category.
    """

    permission_classes = [UserBasedPermission]

    @swagger_auto_schema(request_body=CategoryWriteSerializer)
    def post(self, request, format=None):
        serializer = CategoryWriteSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            restaurant = request.data.get("restaurant")
            obj = Restaurant.objects.get(pk=restaurant)
            self.check_object_permissions(self.request, obj)
            category = serializer.save(created_by=request.user)
            serializer = CategoryReadSerializer(category)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class CategoryDetail(APIView):
    """
    Retrieve, update or delete a category instance.
    """

    permission_classes = [UserBasedPermission]

    def get_object(self, pk):
        try:
            obj = Category.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj.restaurant)
            return obj
        except Category.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategoryReadSerializer(category)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CategoryWriteSerializer)
    def patch(self, request, pk, format=None):
        category = self.get_object(pk)
        serializer = CategoryWriteSerializer(category, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            category = serializer.save(updated_by=request.user)
            serializer = CategoryReadSerializer(category)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        category = self.get_object(pk)
        category.soft_delete()
        reorder_catagories(category.restaurant)
        return Response(status=status.HTTP_204_NO_CONTENT)
