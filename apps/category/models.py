from django.db import models
from authentication.models import CreatorUpdaterModel, TimeStampModel
from apps.restaurant.models import Restaurant


class Category(TimeStampModel, CreatorUpdaterModel):
    restaurant = models.ForeignKey(
        Restaurant, models.PROTECT, related_name="categories"
    )
    name = models.CharField(max_length=120, blank=True, null=True)
    priority = models.PositiveBigIntegerField(default=1)

    def total_item(self):
        return self.items.all().count()

    def __str__(self):
        return self.name

    class Meta:
        db_table = "category"
        ordering = ["priority"]
