from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("courses/", views.Courses_Create.as_view(), name="courses"),
    path("courses/delete/<int:pk>/", views.Course_Delete.as_view(), name="delete-course"),
    path('api/current_user/', views.CurrentUserView.as_view(), name='current_user'),
    path("courses/join/<int:course_id>/", views.JoinCourseView.as_view(), name="join-course"),
    path("courses/<int:course_id>/", views.CourseDetailView.as_view(), name="course-detail"),  # New route for course details
    path("api/teacher-profile/", views.TeacherProfileUpdateView.as_view(), name="teacher-profile-update"),
]