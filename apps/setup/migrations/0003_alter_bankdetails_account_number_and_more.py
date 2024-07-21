# Generated by Django 4.2.3 on 2023-08-14 12:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("setup", "0002_identity_bankdetails"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bankdetails",
            name="account_number",
            field=models.CharField(default=1, max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="identity",
            name="identity_number",
            field=models.IntegerField(default=1, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="identity",
            name="trade_license_number",
            field=models.IntegerField(default=1, unique=True),
            preserve_default=False,
        ),
    ]
