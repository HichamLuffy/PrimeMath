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
    path('teacher-dashboard/', views.TeacherDashboardView.as_view(), name='teacher-dashboard'),
    path('edit-teacher-profile/', views.TeacherProfileUpdateView.as_view(), name='edit-teacher-profile'),
    path('tasks/submit/<int:task_id>/', views.SubmitTaskView.as_view(), name='submit-task'),
    path("projects/<int:project_id>/", views.ProjectDetailView.as_view(), name="project-detail"),
    path('api/users/', views.UserListAPIView.as_view(), name='user-list'),
]