from django.db.models.signals import post_save, post_init
from django.dispatch import receiver
from django.conf import settings
from common.emails import (
    email_verification_mail_request,
    phone_verification_mail_request,
)


# triggers while initializing user
@receiver(post_init, sender=settings.AUTH_USER_MODEL)
def remember_state(sender, instance, **kwargs):
    instance.previous_email = instance.email
    instance.previous_phone = instance.phone


# triggers when user created or signup
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def send_verification_mail(sender, instance, created, **kwargs):
    if created and not instance.is_active:
        email_verification_mail_request(instance)
        phone_verification_mail_request(instance)

    # email if changed
    if (
        instance.previous_email != instance.email
        and not instance.is_email_verified
        and not created
    ):
        email_verification_mail_request(instance)

    # phone no if changed
    if (
        instance.previous_phone != instance.phone
        and not instance.is_phone_verified
        and not created
    ):
        phone_verification_mail_request(instance)
