from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("courses/", views.Courses_Create.as_view(), name="courses"),
    path("courses/delete/<int:pk>/", views.Course_Delete.as_view(), name="delete-course"),
]