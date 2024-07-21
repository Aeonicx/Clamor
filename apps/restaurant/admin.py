from django.contrib import admin
from .models import Restaurant


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    readonly_fields = ["created_by", "updated_by", "deleted_at"]
    list_display = ["id", "name", "user", "contact", "is_active", "created_at"]
