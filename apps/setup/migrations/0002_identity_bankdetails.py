# Generated by Django 4.2.3 on 2023-08-11 07:16

import apps.setup.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms


class Migration(migrations.Migration):
    dependencies = [
        ("restaurant", "0003_alter_restaurant_image"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("setup", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Identity",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "restaurant",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        primary_key=True,
                        serialize=False,
                        to="restaurant.restaurant",
                    ),
                ),
                (
                    "identity_card_image",
                    django_resized.forms.ResizedImageField(
                        blank=True,
                        crop=None,
                        force_format=None,
                        keep_meta=True,
                        null=True,
                        quality=-1,
                        scale=None,
                        size=[1920, 1080],
                        upload_to=apps.setup.models.identity_path_and_rename,
                    ),
                ),
                ("identity_number", models.IntegerField(null=True)),
                (
                    "trade_license_image",
                    django_resized.forms.ResizedImageField(
                        blank=True,
                        crop=None,
                        force_format=None,
                        keep_meta=True,
                        null=True,
                        quality=-1,
                        scale=None,
                        size=[1920, 1080],
                        upload_to=apps.setup.models.trade_path_and_rename,
                    ),
                ),
                ("trade_license_number", models.IntegerField(null=True)),
                ("trade_license_expiry", models.DateTimeField(null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        db_column="created_by",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_creator",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        db_column="updated_by",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_updater",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "identity",
            },
        ),
        migrations.CreateModel(
            name="BankDetails",
            fields=[
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True, null=True)),
                ("deleted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "restaurant",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        primary_key=True,
                        serialize=False,
                        to="restaurant.restaurant",
                    ),
                ),
                ("bank_name", models.CharField(blank=True, max_length=255, null=True)),
                ("account_number", models.IntegerField(null=True, unique=True)),
                ("iban", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        db_column="created_by",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_creator",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        db_column="updated_by",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)s_updater",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "bank_details",
            },
        ),
    ]
