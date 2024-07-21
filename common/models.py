from django.db import models
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class RestoreManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().exclude(deleted_at__isnull=True)


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()
    deleted_objects = RestoreManager()

    def soft_delete(self):
        self.deleted_at = str(timezone.now())
        self.save()

    def restore(self):
        self.deleted_at = None
        self.save()

    class Meta:
        abstract = True
