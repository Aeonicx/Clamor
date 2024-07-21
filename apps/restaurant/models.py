from django.db import models
from authentication.models import User, CreatorUpdaterModel, TimeStampModel
from django_resized import ResizedImageField
from uuid import uuid4
import os


def path_and_rename(instance, filename):
    upload_to = "restaurant/"
    ext = filename.split(".")[-1]
    filename = "{}.{}".format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)


class Restaurant(TimeStampModel, CreatorUpdaterModel):
    user = models.ForeignKey(
        User,
        models.PROTECT,
        limit_choices_to={"is_admin": True},
        related_name="restaurants",
    )
    name = models.CharField(max_length=255, unique=True)
    image = ResizedImageField(
        upload_to=path_and_rename,
        default="restaurant/default.jpg",
        blank=True,
        null=True,
    )
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    zip = models.IntegerField(null=True)
    contact = models.IntegerField(null=True)
    about = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "restaurant"
