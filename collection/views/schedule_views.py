from collection.models import Schedule
from collection.serializers import ScheduleSerializer
from rest_framework.views import APIView
from django.http import Http404
from common.utils import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from common.permissions import IsSuperuserOrReadOnly


class ScheduleList(APIView):
    """
    List all schedules, or create a new schedule.
    """

    permission_classes = [IsSuperuserOrReadOnly]

    def get(self, request, format=None):
        schedules = Schedule.objects.all()
        serializer = ScheduleSerializer(schedules, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ScheduleSerializer)
    def post(self, request, format=None):
        serializer = ScheduleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class ScheduleDetail(APIView):
    """
    Retrieve, update or delete a schedule instance.
    """

    permission_classes = [IsSuperuserOrReadOnly]

    def get_object(self, pk):
        try:
            return Schedule.objects.get(pk=pk)
        except Schedule.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        schedule = self.get_object(pk)
        serializer = ScheduleSerializer(schedule)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=ScheduleSerializer)
    def patch(self, request, pk, format=None):
        schedule = self.get_object(pk)
        serializer = ScheduleSerializer(schedule, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        schedule = self.get_object(pk)
        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
