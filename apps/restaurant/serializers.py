from rest_framework import serializers
from apps.setup.serializers import AvailabilityReadSerializer
from .models import Restaurant
from common.constants import PHONE_VALIDATE_REGEX
import re


class RestaurantReadSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True, allow_empty_file=True)
    availability = AvailabilityReadSerializer(read_only=True)

    class Meta:
        model = Restaurant
        fields = [
            "id",
            "user",
            "name",
            "address",
            "city",
            "state",
            "zip",
            "contact",
            "about",
            "image",
            "availability",
        ]


class RestaurantWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            "id",
            "image",
            "name",
            "address",
            "city",
            "state",
            "zip",
            "contact",
            "about",
        ]
        extra_kwargs = {
            "image": {"required": False, "allow_null": False},
            "name": {"required": True, "allow_blank": False, "allow_null": False},
            "address": {"required": True, "allow_blank": False, "allow_null": False},
            "city": {"required": True, "allow_blank": False, "allow_null": False},
            "state": {"required": True, "allow_blank": False, "allow_null": False},
            "zip": {"required": True, "allow_null": False},
            "contact": {"required": False, "allow_null": False},
            "about": {"required": False, "allow_blank": False, "allow_null": False},
        }

    def validate_contact(self, value):
        # Attempt to match the phone number against the pattern
        if not re.match(PHONE_VALIDATE_REGEX, str(value)):
            raise serializers.ValidationError("Please enter a valid contact.")
        return value

    def validate_zip(self, value):
        # Attempt to match the phone number against the pattern
        if not len(str(value)) == 5:
            raise serializers.ValidationError("Please enter a valid 5 digits zip code.")
        return value

    def create(self, validated_data):
        user = validated_data.get("user")
        if not user.is_admin:
            raise serializers.ValidationError(
                "User is not permitted to perform this action."
            )

        if Restaurant.objects.filter(user=user).exists():
            raise serializers.ValidationError("Restaurant already exist for this user.")
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Remove the field you want to exclude from update
        validated_data.pop("user", None)
        return super().update(instance, validated_data)
