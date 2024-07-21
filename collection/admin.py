from django.contrib import admin
from .models import Cuisine, Dietary, Schedule


@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    readonly_fields = ["deleted_at"]
    list_display = ["id", "name", "updated_at", "created_at"]


@admin.register(Dietary)
class DietaryAdmin(admin.ModelAdmin):
    readonly_fields = ["deleted_at"]
    list_display = ["id", "name", "updated_at", "created_at"]


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    readonly_fields = ["deleted_at"]
    list_display = ["id", "name", "updated_at", "created_at"]
