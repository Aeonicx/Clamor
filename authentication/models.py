from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from common.models import TimeStampModel


class User(AbstractBaseUser, PermissionsMixin, TimeStampModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.IntegerField(unique=True)
    address = models.TextField(blank=True, null=True)
    otp_secret = models.CharField(max_length=255, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone"]

    @property
    def is_active(self):
        return self.is_email_verified

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.name

    class Meta:
        db_table = "user"


class CreatorUpdaterModel(models.Model):
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_creator",
        db_column="created_by",
        blank=True,
        null=True,
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="%(class)s_updater",
        db_column="updated_by",
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True
