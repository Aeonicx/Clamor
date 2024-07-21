from django.urls import path
from . import views

urlpatterns = [
    # Availability
    path("availabilities/", views.AvailabilityList.as_view()),
    path("availabilities/<int:pk>/", views.AvailabilityDetail.as_view()),
    # BankDetails
    path("bank-details/", views.BankDetailsList.as_view()),
    path("bank-details/<int:pk>/", views.BankDetailsDetail.as_view()),
    # Identity
    path("identities/", views.IdentityList.as_view()),
    path("identities/<int:pk>/", views.IdentityDetail.as_view()),
]
