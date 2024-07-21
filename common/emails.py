from django.core.mail import EmailMessage
import threading, pyotp
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from authentication.utils import generate_otp


# default sender
EMAIL_HOST_USER = "Clamor <noreply@clamor.com>"
CLAMOR_ADMIN_MAIL_ID = "admin-clamor@gmail.com"


class EmailThread(threading.Thread):
    def __init__(self, subject, body, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.body = body
        threading.Thread.__init__(self)

    def run(self):
        email = EmailMessage(
            self.subject, self.body, EMAIL_HOST_USER, self.recipient_list
        )
        email.content_subtype = "html"
        max_tries = 3
        tries = 0
        while tries < max_tries:
            try:
                email.send()
                break  # exit the loop if email successfully sent
            except:
                tries += 1


# sending html content email
def send_mail(subject, body, recipient_list):
    EmailThread(subject, body, recipient_list).start()


# sending email-verification mail
def email_verification_mail_request(user):
    subject = "Email verification mail for Clamor"
    token = RefreshToken.for_user(user).access_token
    url = f"{settings.APP_URL}verify-email?token={token}"

    message_html = render_to_string(
        "authentication/email_verification_template.html",
        {
            "user": user,
            "url": url,
            "token": token,
        },
    )
    send_mail(
        subject=subject,
        body=message_html,
        recipient_list=[user.email],
    )


# sending phone-verification mail
def phone_verification_mail_request(user):
    subject = "Phone verification mail for Clamor"
    otp = generate_otp(user)

    message_html = render_to_string(
        "authentication/phone_verification_template.html",
        {
            "user": user,
            "otp": otp,
        },
    )
    send_mail(
        subject=subject,
        body=message_html,
        recipient_list=[user.email],
    )


# sending password-reset mail
def reset_password_mail_request(user):
    subject = "Password reset mail for Clamor"
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = PasswordResetTokenGenerator().make_token(user)
    url = f"{settings.APP_URL}reset-password?uid={uid}&token={token}"

    message_html = render_to_string(
        "authentication/reset_password_template.html",
        {
            "user": user,
            "url": url,
            "token": token,
        },
    )
    send_mail(
        subject=subject,
        body=message_html,
        recipient_list=[user.email],
    )
