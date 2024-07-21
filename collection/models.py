from django.db import models
from authentication.models import TimeStampModel


class Cuisine(TimeStampModel):
    name = models.CharField(max_length=120, unique=True, verbose_name="Name")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "cuisine"
        ordering = ["name"]


class Dietary(TimeStampModel):
    name = models.CharField(max_length=120, unique=True, verbose_name="Name")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "dietary"


class Schedule(TimeStampModel):
    name = models.CharField(max_length=120, unique=True, verbose_name="Name")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "schedule"
