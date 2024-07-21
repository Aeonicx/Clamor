from collection.models import Dietary
from collection.serializers import DietarySerializer
from rest_framework.views import APIView
from django.http import Http404
from common.utils import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from common.permissions import IsSuperuserOrReadOnly


class DietaryList(APIView):
    """
    List all dietaries, or create a new dietary.
    """

    permission_classes = [IsSuperuserOrReadOnly]

    def get(self, request, format=None):
        dietaries = Dietary.objects.all()
        serializer = DietarySerializer(dietaries, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=DietarySerializer)
    def post(self, request, format=None):
        serializer = DietarySerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class DietaryDetail(APIView):
    """
    Retrieve, update or delete a dietary instance.
    """

    permission_classes = [IsSuperuserOrReadOnly]

    def get_object(self, pk):
        try:
            return Dietary.objects.get(pk=pk)
        except Dietary.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        dietary = self.get_object(pk)
        serializer = DietarySerializer(dietary)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=DietarySerializer)
    def patch(self, request, pk, format=None):
        dietary = self.get_object(pk)
        serializer = DietarySerializer(dietary, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        dietary = self.get_object(pk)
        dietary.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
