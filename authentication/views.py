from rest_framework import status
from rest_framework.views import APIView
from common.utils import Response
from .serializers import *
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from .utils import *
import jwt


class UserRegistrationView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        request_body=UserRegistrationSerializer,
        operation_id="user-registration",
    )
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()

            return Response(
                status=status.HTTP_201_CREATED,
                message=f"Hello {user.name}, Your registration is successful. Please verify your email and phone to continue.",
            )


class UserLoginView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        request_body=UserLoginSerializer,
        operation_id="user-login",
    )
    def post(self, request, format=None):

        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            password = serializer.data.get("password")

            user = authenticate(email=email, password=password)
            if user is not None:
                # checking if user's email and phone is verified
                code, message = check_user_verified(user)

                if code is not None:
                    return Response(
                        success=False,
                        status=status.HTTP_401_UNAUTHORIZED,
                        message=message,
                        code=code,
                    )

                token = get_tokens_for_user(user)

                return Response(
                    status=status.HTTP_200_OK,
                    message=f"Hello {user.name}, You have successfully logged in.",
                    token=token,
                )

            return Response(
                success=False,
                status=status.HTTP_401_UNAUTHORIZED,
                message="Invalid Credentials.",
            )


class UserPhoneOTPLoginView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        request_body=UserPhoneOTPLoginSerializer,
        operation_id="user-phone-otp-login",
    )
    def post(self, request, format=None):
        serializer = UserPhoneOTPLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            phone = serializer.data.get("phone")
            otp = serializer.data.get("otp")

            user = User.objects.get(phone=phone)
            # checking if user's email and phone is verified
            code, message = check_user_verified(user)

            if code is not None:
                return Response(
                    success=False,
                    status=status.HTTP_401_UNAUTHORIZED,
                    message=message,
                    code=code,
                )
            elif user.otp_secret is None:
                return Response(
                    success=False,
                    status=status.HTTP_401_UNAUTHORIZED,
                    message="Please request a new OTP to Login.",
                )

            is_otp_valid = verify_otp(user, otp)
            if not is_otp_valid:
                return Response(
                    success=False,
                    status=status.HTTP_401_UNAUTHORIZED,
                    message="Please enter a valid OTP or retry requesting another OTP.",
                )

            token = get_tokens_for_user(user)

            return Response(
                status=status.HTTP_200_OK,
                message=f"Hello {user.name}, You have successfully logged in.",
                token=token,
            )


class UserPhoneOTPLoginRequestView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        request_body=UserPhoneOTPLoginRequestSerializer,
        operation_id="user-phone-otp-login-request",
    )
    def post(self, request, format=None):
        serializer = UserPhoneOTPLoginRequestSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            phone = serializer.data.get("phone")
            user = User.objects.get(phone=phone)

            # checking if user's email and phone is verified
            code, message = check_user_verified(user)

            if code is not None:
                return Response(
                    success=False,
                    status=status.HTTP_401_UNAUTHORIZED,
                    message=message,
                    code=code,
                )

            phone_verification_mail_request(user)
            message = "Login OTP has been sent successfully. Please check your SMS."

            return Response(status=status.HTTP_200_OK, message=message, code=code)


class UserEmailVerificationView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        request_body=UserEmailVerificationSerializer,
        operation_id="user-email-verification",
    )
    def post(self, request, format=None):
        serializer = UserEmailVerificationSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            token = jwt.decode(
                serializer.data.get("token"), settings.SECRET_KEY, algorithms=["HS256"]
            )

            user = User.objects.get(pk=token.get("id"))
            if not user.is_email_verified:
                user.is_email_verified = True
                user.save()
                message = (
                    f"Hello {user.name}, Your email has been verified successfully."
                )
            else:
                message = f"Hello {user.name}, Your email is already verified."

            return Response(
                status=status.HTTP_200_OK,
                message=message,
            )


class UserPhoneVerificationView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        request_body=UserPhoneVerificationSerializer,
        operation_id="user-phone-Verification",
    )
    def post(self, request, format=None):
        serializer = UserPhoneVerificationSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            phone = serializer.data.get("phone")
            otp = serializer.data.get("otp")
            user = User.objects.get(phone=phone)

            is_otp_valid = verify_otp(user, otp)
            if not is_otp_valid:
                return Response(
                    success=False,
                    status=status.HTTP_400_BAD_REQUEST,
                    message="Please enter a valid OTP or retry requesting another OTP.",
                )

            if not user.is_phone_verified:
                user.is_phone_verified = True
                user.save()

            return Response(
                status=status.HTTP_200_OK,
                message=f"Hello {user.name}, Your phone number has been verified successfully.",
            )


class UserEmailVerificationRequestView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        request_body=UserEmailVerificationRequestSerializer,
        operation_id="user-email-verification-request",
    )
    def post(self, request, format=None):
        serializer = UserEmailVerificationRequestSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            return Response(
                status=status.HTTP_200_OK,
                message="Verification mail has been sent successfully. Please check your email.",
            )


class UserPhoneVerificationRequestView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        request_body=UserPhoneVerificationRequestSerializer,
        operation_id="user-phone-verification-request",
    )
    def post(self, request, format=None):
        serializer = UserPhoneVerificationRequestSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            return Response(
                status=status.HTTP_200_OK,
                message="OTP has been sent successfully. Please check your SMS.",
            )


class UserChangePasswordView(APIView):
    @swagger_auto_schema(
        request_body=UserChangePasswordSerializer,
        operation_id="user-change-password",
    )
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={"user": request.user}
        )

        if serializer.is_valid(raise_exception=True):
            return Response(
                status=status.HTTP_200_OK,
                message="Your Account Password has been changed successfully.",
            )


class UserResetPasswordRequestView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        request_body=UserResetPasswordRequestSerializer,
        operation_id="user-reset-password-request",
    )
    def post(self, request, format=None):
        serializer = UserResetPasswordRequestSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            return Response(
                status=status.HTTP_200_OK,
                message="Password reset mail has been sent successfully. Please check your email",
            )


class UserResetPasswordView(APIView):
    permission_classes = []

    @swagger_auto_schema(
        request_body=UserResetPasswordSerializer,
        operation_id="user-reset-password",
    )
    def post(self, request, format=None):
        serializer = UserResetPasswordSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            return Response(
                status=status.HTTP_200_OK,
                message="Your password has been reset successfully. You can login now.",
            )
