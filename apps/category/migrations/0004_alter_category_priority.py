# Generated by Django 4.2.3 on 2023-08-17 07:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("category", "0003_alter_category_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="priority",
            field=models.PositiveBigIntegerField(default=1),
        ),
    ]
