from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
from django.contrib import messages
from .models import Courses, Projects, Profile, StudentProfile, TeacherProfile
from .decorators import student_required, teacher_required
from django.contrib.auth import authenticate, login as django_login
from .serializers import ProfileSerializer, UserSerializer, CoursesSerializer, UserProfileSerializer
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

# Create your views here.

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all() #? this is the list of users to create a new user and make sure they are not already exist
    serializer_class = UserSerializer #? this tell this view what kind of data we need to accept to make a new user 
    permission_classes = [AllowAny] #? specifies who can actually can call this

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

@api_view(['POST'])
def register(request):
    data = request.data
    user_serializer = UserSerializer(data={
        'username': data.get('username'),
        'password': data.get('password'),
        'email': data.get('email')
    })

    if user_serializer.is_valid():
        user = user_serializer.save()
        role = data.get('role')

        profile_serializer = ProfileSerializer(data={'user': user.id, 'role': role})
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        else:
            user.delete()  # Rollback user creation if profile creation fails
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)