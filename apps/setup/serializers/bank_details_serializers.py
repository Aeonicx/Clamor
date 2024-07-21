from rest_framework import serializers
from apps.setup.models import BankDetails
from collection.serializers import *


class BankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetails
        fields = ["restaurant", "bank_name", "account_number", "iban"]
        extra_kwargs = {
            "restaurant": {"required": True, "allow_null": False},
            "bank_name": {"required": True, "allow_blank": False, "allow_null": False},
            "iban": {"required": True, "allow_blank": False, "allow_null": False},
            "account_number": {
                "required": True,
                "allow_blank": False,
                "allow_null": False,
            },
        }

    def validate_account_number(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
                "Account number should only contain digits."
            )
        return value

    def update(self, instance, validated_data):
        # Remove the field you want to exclude from update
        validated_data.pop("restaurant", None)
        return super().update(instance, validated_data)
