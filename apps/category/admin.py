from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = [
        "created_by",
        "updated_by",
        "deleted_at",
    ]
    list_display = [
        "id",
        "restaurant",
        "name",
        "priority",
        "created_at",
    ]
