from collection.models import Cuisine
from collection.serializers import CuisineSerializer
from rest_framework.views import APIView
from django.http import Http404
from common.utils import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from common.permissions import IsSuperuserOrReadOnly


class CuisineList(APIView):
    """
    List all cuisines, or create a new cuisine.
    """

    permission_classes = [IsSuperuserOrReadOnly]

    def get(self, request, format=None):
        cuisines = Cuisine.objects.all()
        serializer = CuisineSerializer(cuisines, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CuisineSerializer)
    def post(self, request, format=None):
        serializer = CuisineSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class CuisineDetail(APIView):
    """
    Retrieve, update or delete a cuisine instance.
    """

    permission_classes = [IsSuperuserOrReadOnly]

    def get_object(self, pk):
        try:
            return Cuisine.objects.get(pk=pk)
        except Cuisine.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        cuisine = self.get_object(pk)
        serializer = CuisineSerializer(cuisine)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CuisineSerializer)
    def patch(self, request, pk, format=None):
        cuisine = self.get_object(pk)
        serializer = CuisineSerializer(cuisine, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        cuisine = self.get_object(pk)
        cuisine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
