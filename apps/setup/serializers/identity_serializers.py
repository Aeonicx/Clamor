from rest_framework import serializers
from apps.setup.models import Identity
from collection.serializers import *


class IdentitySerializer(serializers.ModelSerializer):
    identity_card_image = serializers.ImageField(
        max_length=None, use_url=True, allow_empty_file=True
    )
    trade_license_image = serializers.ImageField(
        max_length=None, use_url=True, allow_empty_file=True
    )

    class Meta:
        model = Identity
        fields = [
            "restaurant",
            "identity_card_image",
            "identity_number",
            "trade_license_image",
            "trade_license_number",
            "trade_license_expiry",
        ]
        extra_kwargs = {
            "restaurant": {"required": True, "allow_null": False},
            "identity_card_image": {"required": True, "allow_null": False},
            "identity_number": {"required": True, "allow_null": False},
            "trade_license_image": {"required": True, "allow_null": False},
            "trade_license_number": {"required": True, "allow_null": False},
            "restaurant": {"required": True, "allow_null": False},
            "trade_license_expiry": {"required": True, "allow_null": False},
        }

    def update(self, instance, validated_data):
        # Remove the field you want to exclude from update
        validated_data.pop("restaurant", None)
        return super().update(instance, validated_data)
