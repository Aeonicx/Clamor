from django.contrib import admin
from .models import BusinessHour, HolidayHour, SpecialOfferHour


@admin.register(BusinessHour)
class BusinessHourAdmin(admin.ModelAdmin):
    readonly_fields = ["deleted_at", "created_by", "updated_by"]
    list_display = [
        "id",
        "restaurant",
        "day",
        "opening_time",
        "closing_time",
        "created_at",
    ]


@admin.register(HolidayHour)
class HolidayHourAdmin(admin.ModelAdmin):
    readonly_fields = ["deleted_at", "created_by", "updated_by"]
    list_display = [
        "id",
        "restaurant",
        "start_datetime",
        "end_datetime",
        "is_active",
        "created_at",
    ]


@admin.register(SpecialOfferHour)
class SpecialOfferHourAdmin(admin.ModelAdmin):
    readonly_fields = ["deleted_at", "created_by", "updated_by"]
    list_display = [
        "id",
        "restaurant",
        "start_datetime",
        "end_datetime",
        "is_active",
        "created_at",
    ]
