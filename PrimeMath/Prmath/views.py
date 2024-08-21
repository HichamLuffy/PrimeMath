from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
from django.contrib import messages
from .models import Courses, Projects, Profile, StudentProfile, TeacherProfile, Subject
from .decorators import student_required, teacher_required
from django.contrib.auth import authenticate, login as django_login
from .serializers import UserSerializer, CoursesSerializer, UserProfileSerializer, ProfileSerializer
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.generics import UpdateAPIView
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
        print(f"Request data: {self.request.data}")
        user = serializer.save()
        role = self.request.data.get('role', 'student')  # Default role to 'student'
        
        # Check if a Profile already exists for this user
        print(f"Role received: {role}")
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

class TeacherProfileUpdateView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        # Return the teacher's profile object for the authenticated user
        return self.request.user.profile.teacherprofile

    def perform_update(self, serializer):
        profile_data = self.request.data
        profile = self.get_object()

        # Update profile with data
        profile.profile.age = profile_data.get('age', profile.profile.age)
        profile.profile.status = profile_data.get('status', profile.profile.status)
        profile.profile.teaching_experience = profile_data.get('teaching_experience', profile.profile.teaching_experience)
        profile.profile.certifications = profile_data.get('certifications', profile.profile.certifications)

        # Update subjects of expertise
        if 'subjects_of_expertise' in profile_data:
            profile.profile.subjects_of_expertise.clear()
            for subject_name in profile_data['subjects_of_expertise']:
                subject, created = Subject.objects.get_or_create(name=subject_name)
                profile.profile.subjects_of_expertise.add(subject)

        profile.profile.save()
        serializer.save()

class Courses_Create(generics.ListCreateAPIView):
    serializer_class = CoursesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Courses.objects.all()

    def get(self, request):
        courses = self.get_queryset()
        user = request.user
        user_courses = user.profile.studentprofile.current_courses.all() if hasattr(user.profile, 'studentprofile') else []
        serialized_courses = CoursesSerializer(courses, many=True).data

        # Mark courses as active based on user-specific enrollment
        for course in serialized_courses:
            course['is_active'] = any(uc.id == course['id'] for uc in user_courses)

        return Response(serialized_courses)

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
        profile_data = {
            'username': user.username,
            'role': user.profile.role,
        }

        if user.profile.role == 'student':
            student_profile = user.profile.studentprofile
            profile_data['points'] = student_profile.points
            profile_data['current_courses'] = [{
                'name': course.name,
                'id': course.id,
            } for course in student_profile.current_courses.all()]
            profile_data['current_projects'] = [{
                'title': project.title,
                'id': project.id,
            } for project in student_profile.current_projects.all()]

        elif user.profile.role == 'teacher':
            teacher_profile = user.profile.teacherprofile
            profile_data['points'] = teacher_profile.points
            profile_data['courses_taught'] = [{
                'name': course.name,
                'id': course.id,
            } for course in teacher_profile.courses_taught.all()]
            profile_data['projects_created'] = [{
                'title': project.title,
                'id': project.id,
            } for project in teacher_profile.projects_created.all()]

        return Response(profile_data)

class CourseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        try:
            course = Courses.objects.get(id=course_id)
            serializer = CoursesSerializer(course)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Courses.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

class JoinCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        try:
            print(f"Joining course with ID: {course_id}")
            course = Courses.objects.get(id=course_id)
            student_profile = request.user.profile.studentprofile

            # Check if the student is already enrolled in the course
            if student_profile.current_courses.filter(id=course_id).exists():
                print("Already enrolled in this course")
                return Response({"error": "You are already enrolled in this course."}, status=status.HTTP_400_BAD_REQUEST)

            student_profile.current_courses.add(course)
            course.number_of_students_in_course += 1
            course.save()

            return Response({"message": "Successfully joined the course"}, status=status.HTTP_200_OK)
        except Courses.DoesNotExist:
            print("Course does not exist")
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return Response({"error": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST)