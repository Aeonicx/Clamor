from rest_framework import serializers
from apps.setup.models import Availability
from collection.serializers import *


class AvailabilityReadSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField(read_only=True)
    order_status = serializers.SerializerMethodField(read_only=True)
    cancellation = serializers.SerializerMethodField(read_only=True)
    cuisines = CuisineSerializer(many=True)
    schedules = ScheduleSerializer(many=True)

    class Meta:
        model = Availability
        fields = [
            "restaurant",
            "cuisines",
            "schedules",
            "status",
            "order_status",
            "cancellation",
            "last_modified_order_status",
        ]

    def get_status(self, obj):
        status = obj.status
        status_display = obj.get_status_display()
        data = {"id": status, "name": status_display}
        return data

    def get_order_status(self, obj):
        order_status = obj.order_status
        order_status_display = obj.get_order_status_display()
        data = {"id": order_status, "name": order_status_display}
        return data

    def get_cancellation(self, obj):
        cancellation = obj.cancellation
        cancellation_display = obj.get_cancellation_display()
        data = {"id": cancellation, "name": cancellation_display}
        return data


class AvailabilityWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = [
            "restaurant",
            "cuisines",
            "schedules",
            "status",
            "order_status",
            "cancellation",
        ]
        extra_kwargs = {
            "restaurant": {"required": True, "allow_null": False},
            "cuisines": {"required": True, "allow_null": False},
            "schedules": {"required": True, "allow_null": False},
            "status": {"required": False, "allow_null": False},
            "order_status": {"required": False, "allow_null": False},
            "cancellation": {"required": False, "allow_null": False},
        }

    def update(self, instance, validated_data):
        # Remove the field you want to exclude from update
        validated_data.pop("restaurant", None)
        return super().update(instance, validated_data)
