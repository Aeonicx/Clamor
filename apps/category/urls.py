from django.urls import path
from .views import *

urlpatterns = [
    path("categories/", CategoryList.as_view()),
    path("categories/<int:pk>/", CategoryDetail.as_view()),
]
