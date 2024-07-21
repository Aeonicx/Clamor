from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.encoding import smart_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from common.constants import PHONE_VALIDATE_REGEX
import jwt, re
from common.emails import (
    email_verification_mail_request,
    phone_verification_mail_request,
    reset_password_mail_request,
)


class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        model = User
        fields = ["name", "email", "phone", "is_admin", "password", "confirm_password"]
        extra_kwargs = {
            "name": {"required": True, "allow_blank": False, "allow_null": False},
            "email": {"required": True, "allow_blank": False, "allow_null": False},
            "phone": {"required": True, "allow_null": False},
            "is_admin": {"required": False, "allow_null": False},
            "password": {
                "write_only": True,
                "required": True,
                "allow_blank": False,
                "allow_null": False,
            },
            "confirm_password": {
                "required": True,
                "allow_blank": False,
                "allow_null": False,
            },
        }

    def validate_email(self, value):
        if User.all_objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError("Email already registered with us.")
        return value.lower()

    def validate_phone(self, value):
        # Attempt to match the phone number against the pattern
        if not re.match(PHONE_VALIDATE_REGEX, str(value)):
            raise serializers.ValidationError("Please enter a valid phone no.")

        return value

    def validate_password(self, value):
        try:
            validate_password(value, self.instance)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError(
                "Password and confirm password doesn't match."
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password", None)
        return User.objects.create_user(**validated_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {
            "email": {"required": True, "allow_blank": False, "allow_null": False},
            "password": {"required": True, "allow_blank": False, "allow_null": False},
        }

    def validate_email(self, value):
        return value.lower()

    def validate(self, attrs):
        email = attrs.get("email")

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Your email address isn't registered with us."
            )

        return attrs


class UserPhoneOTPLoginSerializer(serializers.Serializer):
    phone = serializers.IntegerField()
    otp = serializers.CharField(min_length=6, max_length=6)

    class Meta:
        fields = ["phone", "otp"]
        extra_kwargs = {
            "phone": {"required": True, "allow_null": False},
            "otp": {"required": True, "allow_null": False},
        }

    def validate_phone(self, value):
        # Attempt to match the phone number against the pattern
        if not re.match(PHONE_VALIDATE_REGEX, str(value)):
            raise serializers.ValidationError("Please enter a valid phone no.")

        return value

    def validate_otp(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("OTP should only contain digits.")
        return value

    def validate(self, attrs):
        phone = attrs.get("phone")

        if not User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError(
                "Your phone number isn't registered with us."
            )

        return attrs


class UserEmailVerificationSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)

    class Meta:
        fields = ["token"]
        extra_kwargs = {
            "token": {"required": True, "allow_blank": False, "allow_null": False}
        }

    def validate_token(self, value):
        try:
            token = jwt.decode(value, settings.SECRET_KEY, algorithms=["HS256"])

            if token["token_type"] != "access":
                raise jwt.exceptions.DecodeError

            if not User.objects.filter(pk=token.get("id")).exists():
                raise serializers.ValidationError("No user associated with this token.")

        except jwt.ExpiredSignatureError as identifier:
            raise serializers.ValidationError(
                "Your account verification link has been expired."
            )

        except jwt.exceptions.DecodeError as identifier:
            raise serializers.ValidationError(
                "Your account verification link is not valid."
            )

        return value


class UserPhoneVerificationSerializer(serializers.Serializer):
    phone = serializers.IntegerField()
    otp = serializers.CharField(min_length=6, max_length=6)

    class Meta:
        fields = ["phone", "otp"]
        extra_kwargs = {
            "phone": {"required": True, "allow_null": False},
            "otp": {"required": True, "allow_null": False},
        }

    def validate_phone(self, value):
        # Attempt to match the phone number against the pattern
        if not re.match(PHONE_VALIDATE_REGEX, str(value)):
            raise serializers.ValidationError("Please enter a valid phone no.")

        return value

    def validate_otp(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("OTP should only contain digits.")
        return value

    def validate(self, attrs):
        phone = attrs.get("phone")

        if not User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError(
                "Your Phone number isn't registered with us."
            )
        elif User.objects.filter(phone=phone, is_phone_verified=True).exists():
            raise serializers.ValidationError("Your Phone number is already verified.")

        elif User.objects.filter(phone=phone, otp_secret=None).exists():
            raise serializers.ValidationError("Please request a OTP first to verify.")

        return attrs


class UserEmailVerificationRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ["email"]
        extra_kwargs = {
            "email": {"required": True, "allow_blank": False, "allow_null": False}
        }

    def validate_email(self, value):
        return value.lower()

    def validate(self, attrs):
        email = attrs.get("email")

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Your email address isn't registered with us."
            )
        elif User.objects.filter(email=email, is_email_verified=True).exists():
            raise serializers.ValidationError("Your email is already verified.")
        else:
            user = User.objects.get(email=email)
            email_verification_mail_request(user)

        return attrs


class UserPhoneVerificationRequestSerializer(serializers.Serializer):
    phone = serializers.IntegerField()

    class Meta:
        fields = ["phone"]
        extra_kwargs = {"phone": {"required": True, "allow_null": False}}

    def validate_phone(self, value):
        # Attempt to match the phone number against the pattern
        if not re.match(PHONE_VALIDATE_REGEX, str(value)):
            raise serializers.ValidationError("Please enter a valid phone no.")

        return value

    def validate(self, attrs):
        phone = attrs.get("phone")

        if not User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError(
                "Your Phone number isn't registered with us."
            )
        elif User.objects.filter(phone=phone, is_phone_verified=True).exists():
            raise serializers.ValidationError("Your Phone number is already verified.")
        else:
            user = User.objects.get(phone=phone)
            phone_verification_mail_request(user)

        return attrs


class UserChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    new_password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    confirm_password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        fields = ["old_password", "new_password", "confirm_password"]
        extra_kwargs = {
            "old_password": {
                "required": True,
                "allow_blank": False,
                "allow_null": False,
            },
            "new_password": {
                "required": True,
                "allow_blank": False,
                "allow_null": False,
            },
            "confirm_password": {
                "required": True,
                "allow_blank": False,
                "allow_null": False,
            },
        }

    def validate(self, attrs):
        user = self.context.get("user")

        old_password = attrs.get("old_password")
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        validate_password(new_password, user)

        if new_password != confirm_password:
            raise serializers.ValidationError(
                "New password and confirm password doesn't match."
            )

        elif not user.check_password(old_password):
            raise serializers.ValidationError("Entered password isn't correct.")

        elif old_password == new_password:
            raise serializers.ValidationError(
                "Old password and new password cannot be same."
            )

        user.set_password(new_password)
        user.save()
        return attrs


class UserResetPasswordRequestSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ["email"]
        extra_kwargs = {
            "email": {"required": True, "allow_blank": False, "allow_null": False}
        }

    def validate_email(self, value):
        return value.lower()

    def validate(self, attrs):
        email = attrs.get("email")

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                "Your email address isn't registered with us."
            )
        else:
            user = User.objects.get(email=email)
            reset_password_mail_request(user)

        return attrs


class UserResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField(max_length=255)
    token = serializers.CharField(max_length=255)
    new_password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    confirm_password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    class Meta:
        fields = ["new_password", "confirm_password"]
        extra_kwargs = {
            "uid": {"required": True, "allow_blank": False, "allow_null": False},
            "token": {"required": True, "allow_blank": False, "allow_null": False},
            "new_password": {
                "required": True,
                "allow_blank": False,
                "allow_null": False,
            },
            "confirm_password": {
                "required": True,
                "allow_blank": False,
                "allow_null": False,
            },
        }

    def validate_uid(self, value):
        try:
            decoded_value = smart_str(urlsafe_base64_decode(value))
        except:
            raise serializers.ValidationError("Please enter a valid uid.")

        if not User.objects.filter(pk=decoded_value).exists():
            raise serializers.ValidationError("No user associated with this uid.")

        return value

    def validate(self, attrs):
        uid = attrs.get("uid")
        token = attrs.get("token")
        new_password = attrs.get("new_password")
        confirm_password = attrs.get("confirm_password")

        user = User.objects.get(pk=smart_str(urlsafe_base64_decode(uid)))

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError(
                "Password reset link is invalid or expired."
            )

        validate_password(new_password, user)

        if new_password != confirm_password:
            raise serializers.ValidationError(
                "New password and confirm password doesn't match."
            )

        user.set_password(new_password)
        user.save()
        return attrs


class UserPhoneOTPLoginRequestSerializer(serializers.Serializer):
    phone = serializers.IntegerField()

    class Meta:
        fields = ["phone"]
        extra_kwargs = {"phone": {"required": True, "allow_null": False}}

    def validate_phone(self, value):
        # Attempt to match the phone number against the pattern
        if not re.match(PHONE_VALIDATE_REGEX, str(value)):
            raise serializers.ValidationError("Please enter a valid phone no.")

        return value

    def validate(self, attrs):
        phone = attrs.get("phone")

        if not User.objects.filter(phone=phone).exists():
            raise serializers.ValidationError(
                "Your Phone number isn't registered with us."
            )

        return attrs
