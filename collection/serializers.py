from rest_framework import serializers
from .models import Cuisine, Dietary, Schedule


class CuisineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cuisine
        fields = ["id", "name"]


class DietarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Dietary
        fields = ["id", "name"]


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ["id", "name"]
