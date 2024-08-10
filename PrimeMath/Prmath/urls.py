from django.urls import path
from . import views

urlpatterns = [
    path('<int:id>', views.student_dashboard, name='main'),  # Main page route
    path('Login', views.Login, name='Login'),
    path('Register', views.Register, name='Register'),
    path('Courses', views.Courses_page, name='Courses'),
    path('Dashboard', views.Dashboard, name='Dashboard'),
    path('Profile', views.Profile, name='Profile'),
    path('Users', views.Users, name='Users'),
]