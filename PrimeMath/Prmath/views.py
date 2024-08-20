from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
from django.contrib import messages
from .models import Courses, Projects, Profile, StudentProfile, TeacherProfile
from .decorators import student_required, teacher_required
from django.contrib.auth import authenticate, login as django_login
from .serializers import UserSerializer, CoursesSerializer, UserProfileSerializer, ProfileSerializer
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import IntegrityError

# Create your views here.

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        print("start perform create")
        user = serializer.save()
        role = self.request.data.get('role', 'student')  # Default role to 'student'
        
        # Check if a Profile already exists for this user
        print("the role is", role)
        profile, created = Profile.objects.get_or_create(user=user, defaults={'role': role})
        
        if created:
            try:
                # Create the corresponding extended profile
                if role == 'student':
                    StudentProfile.objects.create(profile=profile)
                elif role == 'teacher':
                    TeacherProfile.objects.create(profile=profile)
                
                print(f"User created with username: {user.username}, role: {role}")
            except IntegrityError as e:
                print(f"IntegrityError: {e}")
                # Optionally, you can handle this error to ensure that duplicate profiles aren't created.
        else:
            if not profile.role:
                profile.role = role
                try:
                # Create the corresponding extended profile
                    if role == 'student':
                        StudentProfile.objects.create(profile=profile)
                    elif role == 'teacher':
                        TeacherProfile.objects.create(profile=profile)
                    
                    print(f"User created with username: {user.username}, role: {role}")
                except IntegrityError as e:
                    print(f"IntegrityError: {e}")
                profile.save()
            print(f"Profile for user {user.username} already exists.")


class Courses_Create(generics.ListCreateAPIView):
    serializer_class = CoursesSerializer
    permission_classes = [IsAuthenticated] #? you can't pass to this root until you are authenticated

    def get(self, request):
        user = request.user
        profile = user.profile
        role = profile.role
        if role == 'student':
            student_profile = StudentProfile.objects.get(profile=profile)
            role_data = {'role': role}
        elif role == 'teacher':
            teacher_profile = TeacherProfile.objects.get(profile=profile)
            role_data = {'role': role}
        else:
            role_data = {'role': 'unknown'}

        user_data = {
            'username': user.username,
            'email': user.email,
            'profile': role_data
        }
        return Response(user_data)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(teacher_owner=self.request.user)
        else:
            print(serializer.errors)

class Course_Delete(generics.DestroyAPIView):
    serializer_class = CoursesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Courses.objects.filter(teacher_owner=user)

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)

