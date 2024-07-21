from rest_framework_simplejwt.tokens import RefreshToken
from common.constants import DEFAULT_OTP_TIME
import pyotp


# manual generating tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


# checking if user's email and phone is verified
def check_user_verified(user):
    code = None
    message = "Verified user"

    if not user.is_email_verified:
        message = f"Hello {user.name}, Please verify your registered email address to continue login."
        code = "email_verification"

    elif not user.is_phone_verified:
        message = f"Hello {user.name}, Please verify your registered phone number to continue login."
        code = "phone_verification"

    return code, message


# Random 6 digits OTP generating for user
def generate_otp(user):
    # random otp generating
    totp = pyotp.TOTP(pyotp.random_base32(), interval=DEFAULT_OTP_TIME)
    otp = totp.now().zfill(6)
    secret = totp.secret

    # storing otp_secret to user object
    user.otp_secret = secret
    user.save()
    return otp


# if OTP matched then return True else False
def verify_otp(user, otp):
    otp_secret = user.otp_secret
    totp = pyotp.TOTP(otp_secret, interval=DEFAULT_OTP_TIME)

    if not totp.verify(otp):
        return False

    # removing otp_secret from user object
    user.otp_secret = None
    user.save()
    return True
