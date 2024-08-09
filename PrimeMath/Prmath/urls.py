from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),  # Main page route
    path('Login', views.Login, name='Login'),
    path('Register', views.Register, name='Register'),
    path('Courses', views.Courses, name='Courses'),
    path('Dashboard', views.Dashboard, name='Dashboard'),
    path('Profile', views.Profile, name='Profile'),
    path('Users', views.Users, name='Users'),
]