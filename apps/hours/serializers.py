from rest_framework import serializers
from .models import BusinessHour, HolidayHour, SpecialOfferHour


class BusinessHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessHour
        fields = [
            "id",
            "restaurant",
            "day",
            "opening_time",
            "closing_time",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def validate(self, attrs):
        opening_time = attrs.get("opening_time", None)
        closing_time = attrs.get("closing_time", None)

        if opening_time and closing_time:
            if not closing_time > opening_time:
                raise serializers.ValidationError(
                    "Closing time should be greater than opening time."
                )

        return super().validate(attrs)

    def update(self, instance, validated_data):
        opening_time = validated_data.get("opening_time", instance.opening_time)
        closing_time = validated_data.get("closing_time", instance.closing_time)

        if not closing_time > opening_time:
            raise serializers.ValidationError(
                "Closing time should be greater than opening time."
            )

        # Remove the field you want to exclude from update
        validated_data.pop("restaurant", None)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update([("day", {"id": instance.day, "name": instance.get_day_display()})])
        return data


class HolidayHourSerializer(serializers.ModelSerializer):
    class Meta:
        model = HolidayHour
        fields = [
            "id",
            "restaurant",
            "start_datetime",
            "end_datetime",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["is_active", "created_at", "updated_at"]

    def validate(self, attrs):
        start_datetime = attrs.get("start_datetime", None)
        end_datetime = attrs.get("end_datetime", None)

        if start_datetime and end_datetime:
            if not end_datetime > start_datetime:
                raise serializers.ValidationError(
                    "End datetime should be greater than start datetime."
                )

        return super().validate(attrs)

    def update(self, instance, validated_data):
        start_datetime = validated_data.get("start_datetime", instance.start_datetime)
        end_datetime = validated_data.get("end_datetime", instance.end_datetime)

        if start_datetime and end_datetime:
            if not end_datetime > start_datetime:
                raise serializers.ValidationError(
                    "End datetime should be greater than start datetime."
                )

        # Remove the field you want to exclude from update
        validated_data.pop("restaurant", None)
        return super().update(instance, validated_data)
