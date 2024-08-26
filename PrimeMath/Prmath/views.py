from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
from django.contrib import messages
from .models import Courses, Projects, Profile, StudentProfile, TeacherProfile, Subject, Tasks
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
from django.utils import timezone
from django.shortcuts import get_object_or_404

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

class TeacherDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not hasattr(user.profile, 'teacherprofile'):
            return Response({"error": "Not authorized"}, status=403)

        teacher_profile = user.profile.teacherprofile
        students = StudentProfile.objects.all().values('profile__user__username', 'profile__user__id')

        profile_data = {
            'teaching_experience': teacher_profile.teaching_experience,
            'certifications': teacher_profile.certifications,
        }

        return Response({
            'profile': profile_data,
            'students': [{'name': student['profile__user__username'], 'id': student['profile__user__id']} for student in students]
        })

class Courses_Create(generics.ListCreateAPIView):
    serializer_class = CoursesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Courses.objects.all()

    def get(self, request):
        courses = self.get_queryset().order_by('id')
        user = request.user
        user_courses = user.profile.studentprofile.current_courses.all() if hasattr(user.profile, 'studentprofile') else []
        
        serialized_courses = CoursesSerializer(courses, many=True).data
        
        # Automatically make the first course active
        if serialized_courses:
            serialized_courses[0]['is_active'] = True

        # Check for course completion and enable the next course if the previous is completed
        for i in range(len(serialized_courses)):
            current_course = serialized_courses[i]
            if any(uc.id == current_course['id'] for uc in user_courses):
                current_course['is_active'] = True

        return Response(serialized_courses)


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
            projects = course.projects_set.all()
            project_data = [{
                'id': project.id,
                'title': project.title,
                'description': project.description,
            } for project in projects]

            course_data = {
                'name': course.name,
                'description': course.description,
                'is_active': course.is_active,
                'number_of_students_in_course': course.number_of_students_in_course,
                'date_created': course.date_created,
                'date_updated': course.date_updated,
                'projects': project_data,
                'score': course.score,

            }

            return Response(course_data)
        except Courses.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)


class JoinCourseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        try:
            course = Courses.objects.get(id=course_id)
            student_profile = request.user.profile.studentprofile

            # Fetch the previous course in the sequence, if any
            previous_course = Courses.objects.filter(id=course_id - 1).first()

            # Check if the student is already enrolled in the course
            if student_profile.current_courses.filter(id=course_id).exists():
                return Response({"error": "You are already enrolled in this course."}, status=status.HTTP_400_BAD_REQUEST)

            # Ensure the previous course is completed if it exists
            if previous_course and not student_profile.current_courses.filter(id=previous_course.id, is_completed=True).exists():
                return Response({"error": "You need to complete the previous course before joining this one."}, status=status.HTTP_400_BAD_REQUEST)

            student_profile.current_courses.add(course)
            course.number_of_students_in_course += 1
            course.save()

            return Response({"message": "Successfully joined the course"}, status=status.HTTP_200_OK)
        except Courses.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_id):
        try:
            project = Projects.objects.get(id=project_id)
            tasks = project.tasks_set.all()
            task_data = [{
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'question': task.question,
                'options': task.options,
            } for task in tasks]

            project_data = {
                'title': project.title,
                'description': project.description,
                'tasks': task_data,
                'is_completed': project.is_completed,
                'defficulty_level': project.difficulty_level,
            }

            return Response(project_data)
        except Projects.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)


class SubmitTaskView(APIView):
    def post(self, request, task_id):
        task = get_object_or_404(Tasks, id=task_id)
        chosen_answer = request.data.get('chosen_answer')

        if not chosen_answer:
            return Response({"error": "No answer provided"}, status=400)

        task.chosen_answer = chosen_answer

        if task.check_answer(chosen_answer):
            task.mark_as_completed()
            return Response({"message": "Correct! The task is marked as completed.", "is_completed": True})
        else:
            return Response({"message": "Incorrect. Try again!", "is_completed": False})


class UserListAPIView(APIView):
    def get(self, request):
        users_data = []
        users = User.objects.all()

        for user in users:
            try:
                profile = user.profile
                online_status = profile.is_online()
                score = profile.studentprofile.points if hasattr(profile, 'studentprofile') else 0
            except Profile.DoesNotExist:
                online_status = False
                score = 0
            
            users_data.append({
                "username": user.username,
                "score": score,
                "online": online_status,
            })

        return Response(users_data)