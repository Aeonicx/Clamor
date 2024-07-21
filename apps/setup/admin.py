from django.contrib import admin
from .models import Availability, Identity, BankDetails


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    readonly_fields = [
        "last_modified_order_status",
        "created_by",
        "updated_by",
        "deleted_at",
    ]
    list_display = [
        "pk",
        "restaurant",
        "status",
        "order_status",
        "cancellation",
        "created_at",
    ]


@admin.register(Identity)
class IdentityAdmin(admin.ModelAdmin):
    readonly_fields = [
        "created_by",
        "updated_by",
        "deleted_at",
    ]
    list_display = [
        "pk",
        "restaurant",
        "identity_number",
        "trade_license_number",
        "created_at",
    ]


@admin.register(BankDetails)
class BankDetailsAdmin(admin.ModelAdmin):
    readonly_fields = [
        "created_by",
        "updated_by",
        "deleted_at",
    ]
    list_display = [
        "pk",
        "restaurant",
        "bank_name",
        "account_number",
        "iban",
        "created_at",
    ]
