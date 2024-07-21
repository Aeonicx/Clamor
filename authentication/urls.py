from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from .views import *

urlpatterns = [
    path("login/", UserLoginView.as_view()),
    path("otp-login/", UserPhoneOTPLoginView.as_view()),
    path("otp-login/request/", UserPhoneOTPLoginRequestView.as_view()),
    path("token/", TokenRefreshView.as_view()),
    path("register/", UserRegistrationView.as_view()),
    path("verify-email/", UserEmailVerificationView.as_view()),
    path("verify-email/request/", UserEmailVerificationRequestView.as_view()),
    path("verify-phone/", UserPhoneVerificationView.as_view()),
    path("verify-phone/request/", UserPhoneVerificationRequestView.as_view()),
    path("password/reset/request/", UserResetPasswordRequestView.as_view()),
    path("password/reset/", UserResetPasswordView.as_view()),
    path("password/change/", UserChangePasswordView.as_view()),
]
