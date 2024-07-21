from rest_framework import serializers
from .models import Category
from .utils import update_category_priority


class CategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "restaurant", "name", "priority", "created_at"]


class CategoryWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "restaurant", "name", "priority"]
        extra_kwargs = {
            "restaurant": {"required": True, "allow_null": False},
            "name": {"required": True, "allow_blank": False, "allow_null": False},
            "priority": {"required": False, "allow_null": False},
        }

    def validate_priority(self, value):
        if value <= 0:
            raise serializers.ValidationError("Value should be greater than 0.")
        return value

    def create(self, validated_data):
        # Remove the field you want to exclude from update
        validated_data.pop("priority", None)

        restaurant = validated_data.get("restaurant")
        name = validated_data.get("name")

        # validating name of category
        if Category.objects.filter(restaurant=restaurant, name=name).exists():
            raise serializers.ValidationError(
                {"name": ["Category name must be unique."]}
            )

        # Retrieve categories ordering by priority descending
        categories = Category.objects.filter(restaurant=restaurant).order_by(
            "-priority"
        )

        if categories.exists():
            # Retrieve the fast category's priority from the categories
            priority = categories.first().priority
            # initializing priority by adding one
            validated_data.update({"priority": priority + 1})

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Remove the field you want to exclude from update
        validated_data.pop("restaurant", None)
        restaurant = instance.restaurant

        # validating name of category
        name = validated_data.get("name", instance.name)
        if (
            Category.objects.filter(restaurant=restaurant, name=name)
            .exclude(pk=instance.pk)
            .exists()
        ):
            raise serializers.ValidationError(
                {"name": ["Category name must be unique."]}
            )

        # validating priority
        priority = validated_data.get("priority", None)
        if priority is not None:
            count = Category.objects.filter(restaurant=restaurant).count()
            if priority > count:
                raise serializers.ValidationError(
                    {"priority": [f"Value should be less or equal to {count}."]}
                )

        # updating priority
        priority = validated_data.get("priority", None)
        if (
            Category.objects.filter(restaurant=restaurant, priority=priority)
            .exclude(pk=instance.pk)
            .exists()
        ):
            update_category_priority(instance, priority)

        return super().update(instance, validated_data)
