from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>', views.student_dashboard, name='main'),  # Main page route
    path('api/login/', views.login_user, name='login_user'),
    path('api/register/', views.register_user, name='register_user'),
    path('Courses', views.Courses_page, name='Courses'),
    path('Dashboard', views.Dashboard, name='Dashboard'),
    path('Profile', views.Profile, name='Profile'),
    path('Users', views.Users, name='Users'),
]