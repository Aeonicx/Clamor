# Generated by Django 4.2.3 on 2023-08-11 14:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("restaurant", "0003_alter_restaurant_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="restaurant",
            name="user",
            field=models.ForeignKey(
                limit_choices_to={"is_admin": True},
                on_delete=django.db.models.deletion.PROTECT,
                related_name="restaurants",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
