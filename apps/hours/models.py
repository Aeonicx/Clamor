from django.db import models
from authentication.models import TimeStampModel, CreatorUpdaterModel
from apps.restaurant.models import Restaurant
from common.constants import DAY_CHOICES


class BusinessHour(TimeStampModel, CreatorUpdaterModel):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.PROTECT, related_name="business_hours"
    )
    day = models.IntegerField(choices=DAY_CHOICES, null=1)
    opening_time = models.TimeField(null=True)
    closing_time = models.TimeField(null=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.get_day_display()}: {self.opening_time} - {self.closing_time}"

    class Meta:
        db_table = "business_hour"
        unique_together = (("restaurant", "day"),)
        ordering = ["day"]


class HolidayHour(TimeStampModel, CreatorUpdaterModel):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.PROTECT, related_name="holiday_hours"
    )
    start_datetime = models.DateTimeField(null=True)
    end_datetime = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.start_datetime} to {self.end_datetime}"

    class Meta:
        db_table = "holiday_hour"


class SpecialOfferHour(TimeStampModel, CreatorUpdaterModel):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.PROTECT,
        related_name="special_offer_hours",
    )
    start_datetime = models.DateTimeField(null=True)
    end_datetime = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.restaurant.name} - {self.start_datetime} to {self.end_datetime}"

    class Meta:
        db_table = "special_offer_hour"
