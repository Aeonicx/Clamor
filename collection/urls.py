from django.urls import path
from . import views

urlpatterns = [
    # Cuisine
    path("cuisines/", views.CuisineList.as_view()),
    path("cuisines/<int:pk>/", views.CuisineDetail.as_view()),
    # Dietary
    path("dietaries/", views.DietaryList.as_view()),
    path("dietaries/<int:pk>/", views.DietaryDetail.as_view()),
    # Schedule
    path("schedules/", views.ScheduleList.as_view()),
    path("schedules/<int:pk>/", views.ScheduleDetail.as_view()),
]
