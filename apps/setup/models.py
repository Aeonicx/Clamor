from django.db import models
from authentication.models import CreatorUpdaterModel, TimeStampModel
from apps.restaurant.models import Restaurant
from collection.models import Cuisine, Schedule
from django_resized import ResizedImageField
from django.utils import timezone
from common.constants import AVAILABILITY_STATUS_CHOICES, DEFAULT_STATUS_CHOICES
from uuid import uuid4
import os


def identity_path_and_rename(instance, filename):
    upload_to = "identity_card/"
    ext = filename.split(".")[-1]
    filename = "{}.{}".format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)


def trade_path_and_rename(instance, filename):
    upload_to = "trade_license/"
    ext = filename.split(".")[-1]
    filename = "{}.{}".format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)


class Availability(TimeStampModel, CreatorUpdaterModel):
    restaurant = models.OneToOneField(
        Restaurant, models.PROTECT, primary_key=True, related_name="availability"
    )
    # TODO
    cuisines = models.ManyToManyField(Cuisine)
    schedules = models.ManyToManyField(Schedule)

    status = models.IntegerField(choices=AVAILABILITY_STATUS_CHOICES, default=1)
    order_status = models.IntegerField(choices=DEFAULT_STATUS_CHOICES, default=1)
    last_modified_order_status = models.DateTimeField(null=True)
    cancellation = models.IntegerField(choices=DEFAULT_STATUS_CHOICES, default=1)

    def __str__(self):
        return f"{self.restaurant.name} - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        if self.pk:  # On update
            if Availability.objects.filter(pk=self.pk).exists():
                instance = Availability.objects.get(pk=self.pk)
                if instance.order_status != self.order_status:  # order_status changed
                    self.last_modified_order_status = timezone.now()
            else:
                self.last_modified_order_status = timezone.now()
        else:  # On create
            self.last_modified_order_status = timezone.now()

        super().save(*args, **kwargs)

    class Meta:
        db_table = "availability"


class Identity(TimeStampModel, CreatorUpdaterModel):
    restaurant = models.OneToOneField(Restaurant, models.PROTECT, primary_key=True)
    identity_card_image = ResizedImageField(
        upload_to=identity_path_and_rename, blank=True, null=True
    )
    identity_number = models.IntegerField(unique=True)
    trade_license_image = ResizedImageField(
        upload_to=trade_path_and_rename, blank=True, null=True
    )
    trade_license_number = models.IntegerField(unique=True)
    trade_license_expiry = models.DateTimeField(null=True)

    def __str__(self):
        return self.restaurant.name

    class Meta:
        db_table = "identity"


class BankDetails(TimeStampModel, CreatorUpdaterModel):
    restaurant = models.OneToOneField(Restaurant, models.PROTECT, primary_key=True)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=255, unique=True)
    iban = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.restaurant.name

    class Meta:
        db_table = "bank_details"
