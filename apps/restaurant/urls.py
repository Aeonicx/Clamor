from django.urls import path
from .views import *

urlpatterns = [
    path("restaurants/profile/", RestaurantProfile.as_view()),
    path("restaurants/", RestaurantList.as_view()),
    path("restaurants/<int:pk>/", RestaurantDetail.as_view()),
    path("restaurants/<int:pk>/business-hours/", RestaurantBusinessHourList.as_view()),
    path("restaurants/<int:pk>/holiday-hours/", RestaurantHolidayHourList.as_view()),
    path("restaurants/<int:pk>/categories/", RestaurantCategoryList.as_view()),
]
