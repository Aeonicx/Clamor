from django.urls import path
from . import views

urlpatterns = [
    # BusinessHour
    path("business-hours/", views.BusinessHourList.as_view()),
    path("business-hours/<int:pk>/", views.BusinessHourDetail.as_view()),
    # HolidayHourList
    path("holiday-hours/", views.HolidayHourList.as_view()),
    path("holiday-hours/<int:pk>/", views.HolidayHourDetail.as_view()),
]
