from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ["groups", "user_permissions"]
    readonly_fields = ["last_login", "deleted_at"]

    list_display = [
        "id",
        "name",
        "email",
        "phone",
        "is_active",
        "is_admin",
        "is_superuser",
        "last_login",
        "created_at",
    ]
