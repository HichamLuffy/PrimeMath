from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
from django.contrib import messages
from .models import Courses, Projects, Profile, StudentProfile, TeacherProfile, Subject, Tasks, TaskCompletion
from .decorators import student_required, teacher_required
from django.contrib.auth import authenticate, login as django_login
from .serializers import UserSerializer, CoursesSerializer, UserProfileSerializer, ProfileSerializer, StudentProfileSerializer, TeacherProfileSerializer
from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.generics import UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import IntegrityError
from django.utils import timezone
from django.shortcuts import get_object_or_404
from math import floor
import logging
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import ValidationError

# Create your views here.

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        role = self.request.data.get('role', 'student')  # Default role to 'student'
        
        # Check if a Profile already exists for this user
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
        completed_courses = user.profile.studentprofile.completed_courses.all() if hasattr(user.profile, 'studentprofile') else []

        serialized_courses = []
        previous_course_completed = True  # Initially allow the first course to be joined

        for i, course in enumerate(courses):
            projects = course.projects_set.all()

            total_projects_count = projects.count()
            total_completion_percentage = 0

            for project in projects:
                tasks = project.tasks_set.all()
                total_tasks_count = tasks.count()

                if total_tasks_count > 0:
                    completed_tasks_count = TaskCompletion.objects.filter(
                        user=request.user, task__in=tasks, is_completed=True).count()
                    project_completion_percentage = (completed_tasks_count / total_tasks_count) * 100
                else:
                    project_completion_percentage = 0

                total_completion_percentage += project_completion_percentage

            course_completion_percentage = total_completion_percentage / total_projects_count if total_projects_count > 0 else 0

            is_active = (user_courses.filter(id=course.id).exists() or
                         (previous_course_completed and course.is_active))

            serialized_courses.append({
                'id': course.id,
                'name': course.name,
                'is_active': is_active,
                'number_of_students_in_course': course.number_of_students_in_course,
                'completion_percentage': course_completion_percentage
            })

            # Update the course completion status
            if course_completion_percentage >= 60:
                user.profile.studentprofile.completed_courses.add(course)
                course.is_completed = True
                course.save()

                # Activate the next course if available
                if i + 1 < len(courses):
                    next_course = courses[i + 1]
                    next_course.is_active = True
                    next_course.save()

            previous_course_completed = course_completion_percentage >= 60

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
        profile = user.profile
        profile_data = {
            'username': user.username,
            'role': user.profile.role,
            'email': user.email,
            'age': profile.age,
            'social_links': profile.social_links,
            'last_seen': profile.last_seen,
            'status': profile.status,
            'certifications': profile.certifications,
            'teaching_experience': profile.teaching_experience,
            'subjects_of_expertise': profile.subjects_of_expertise.all().values_list('name', flat=True),
            'profile_pic': profile.profile_pic.url if profile.profile_pic else None,
        }

        if user.profile.role == 'student':
            student_profile = user.profile.studentprofile
            profile_data.update({
                'level': student_profile.level,
                'current_study': student_profile.current_study,
                'completed_courses': student_profile.completed_courses.all().values_list('name', flat=True),
                'skills': student_profile.skills.all().values_list('name', flat=True),
            })

            # Calculate course completion percentages
            current_courses = student_profile.current_courses.all()
            course_completion_list = []
            total_course_completion = 0
            for course in current_courses:
                projects = course.projects_set.all()
                total_projects = projects.count()
                project_completion_total = 0

                for project in projects:
                    tasks = project.tasks_set.all()
                    total_tasks = tasks.count()
                    if total_tasks > 0:
                        completed_tasks = TaskCompletion.objects.filter(user=user, task__in=tasks, is_completed=True).count()
                        project_completion_percentage = (completed_tasks / total_tasks) * 100
                    else:
                        project_completion_percentage = 0
                    project_completion_percentage = min(project_completion_percentage, 100)  # cap at 100%
                    project_completion_total += project_completion_percentage

                if total_projects > 0:
                    course_completion_percentage = project_completion_total / total_projects
                else:
                    course_completion_percentage = 0
                course_completion_percentage = min(course_completion_percentage, 100)  # cap at 100%

                course_completion_list.append({
                    'id': course.id,
                    'name': course.name,
                    'completion_percentage': round(course_completion_percentage, 2)
                })
                total_course_completion += course_completion_percentage

            # Calculate average course completion
            if current_courses.count() > 0:
                average_course_completion = total_course_completion / current_courses.count()
            else:
                average_course_completion = 0

            # Calculate project completion percentages
            current_projects = student_profile.current_projects.all()
            project_completion_list = []
            total_project_completion = 0
            for project in current_projects:
                tasks = project.tasks_set.all()
                total_tasks = tasks.count()
                if total_tasks > 0:
                    completed_tasks = TaskCompletion.objects.filter(user=user, task__in=tasks, is_completed=True).count()
                    project_completion_percentage = (completed_tasks / total_tasks) * 100
                else:
                    project_completion_percentage = 0
                project_completion_percentage = min(project_completion_percentage, 100)  # cap at 100%
                project_completion_list.append({
                    'id': project.id,
                    'title': project.title,
                    'completion_percentage': round(project_completion_percentage, 2)
                })
                total_project_completion += project_completion_percentage

            # Calculate average project completion
            if current_projects.count() > 0:
                average_project_completion = total_project_completion / current_projects.count()
            else:
                average_project_completion = 0

            profile_data['current_courses'] = course_completion_list
            profile_data['current_projects'] = project_completion_list

            # Level Calculation Algorithm
            points = student_profile.points
            bonus_points_courses = (average_course_completion // 10) * 10
            bonus_points_projects = (average_project_completion // 10) * 5
            total_progress_score = points + bonus_points_courses + bonus_points_projects

            # Calculate level and progress to next level
            level = max(floor(total_progress_score / 100) + 1, student_profile.level)
            progress_to_next_level = (total_progress_score % 100) / 100 * 100

            # Ensure progress_to_next_level does not exceed 100
            progress_to_next_level = min(progress_to_next_level, 100)

            # Update level if it has increased
            if level > student_profile.level:
                student_profile.level = level
                student_profile.save()

            profile_data['level'] = level
            profile_data['level_progress'] = round(progress_to_next_level, 2)

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

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        print(f"Fetching profile for username: {username}")  # Debugging

        user = get_object_or_404(User, username=username)
        print(f"Found user: {user.username}")  # Debugging

        profile = user.profile
        print(f"User profile: {profile}")  # Debugging

        profile_data = {
            'username': user.username,
            'role': user.profile.role,
            'email': user.email,
            'age': profile.age,
            'social_links': profile.social_links,
            'last_seen': profile.last_seen,
            'status': profile.status,
            'certifications': profile.certifications,
            'teaching_experience': profile.teaching_experience,
            'subjects_of_expertise': profile.subjects_of_expertise.all().values_list('name', flat=True),
            'profile_pic': profile.profile_pic.url if profile.profile_pic else None,
        }
        print(f"Initial profile data: {profile_data}")  # Debugging

        if user.profile.role == 'student':
            student_profile = user.profile.studentprofile
            print(f"Student profile: {student_profile}")  # Debugging

            profile_data.update({
                'level': student_profile.level,
                'current_study': student_profile.current_study,
                'completed_courses': student_profile.completed_courses.all().values_list('name', flat=True),
                'skills': student_profile.skills.all().values_list('name', flat=True),
            })
            print(f"Updated profile data for student: {profile_data}")  # Debugging

        elif user.profile.role == 'teacher':
            teacher_profile = user.profile.teacherprofile
            print(f"Teacher profile: {teacher_profile}")  # Debugging

            profile_data.update({
                'points': teacher_profile.points,
                'courses_taught': [{
                    'name': course.name,
                    'id': course.id,
                } for course in teacher_profile.courses_taught.all()],
                'projects_created': [{
                    'title': project.title,
                    'id': project.id,
                } for project in teacher_profile.projects_created.all()],
            })
            print(f"Updated profile data for teacher: {profile_data}")  # Debugging

        print(f"Final profile data being returned: {profile_data}")  # Debugging
        return Response(profile_data)


class CourseDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        try:
            course = Courses.objects.get(id=course_id)
            projects = course.projects_set.all()

            total_projects_count = projects.count()
            total_completion_percentage = 0

            project_data = []

            for project in projects:
                tasks = project.tasks_set.all()
                total_tasks_count = tasks.count()

                # Calculate user-specific completion percentage for this project
                if total_tasks_count > 0:
                    completed_tasks_count = TaskCompletion.objects.filter(
                        user=request.user, task__in=tasks, is_completed=True).count()
                    project_completion_percentage = (completed_tasks_count / total_tasks_count) * 100
                else:
                    project_completion_percentage = 0

                total_completion_percentage += project_completion_percentage

                project_data.append({
                    'id': project.id,
                    'title': project.title,
                    'description': project.description,
                    'completion_percentage': project_completion_percentage
                })

            # Calculate the overall course completion percentage
            course_completion_percentage = total_completion_percentage / total_projects_count if total_projects_count > 0 else 0

            course_data = {
                'name': course.name,
                'description': course.description,
                'is_active': course.is_active,
                'number_of_students_in_course': course.number_of_students_in_course,
                'date_created': course.date_created,
                'date_updated': course.date_updated,
                'projects': project_data,
                'completion_percentage': course_completion_percentage,  # Updated completion percentage
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

            previous_course = Courses.objects.filter(id=course_id - 1).first()

            if student_profile.current_courses.filter(id=course_id).exists():
                return Response({"error": "You are already enrolled in this course."}, status=status.HTTP_400_BAD_REQUEST)

            if previous_course and not student_profile.completed_courses.filter(id=previous_course.id).exists():
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

            # Calculate user-specific completion percentage
            completed_tasks_count = TaskCompletion.objects.filter(user=request.user, task__in=tasks, is_completed=True).count()
            total_tasks_count = tasks.count()
            completion_percentage = (completed_tasks_count / total_tasks_count) * 100 if total_tasks_count > 0 else 0

            task_data = []
            for task in tasks:
                is_completed = TaskCompletion.objects.filter(user=request.user, task=task, is_completed=True).exists()
                task_data.append({
                    'id': task.id,
                    'title': task.title,
                    'question': task.question,
                    'options': task.options,
                    'is_completed': is_completed,
                })

            project_data = {
                'title': project.title,
                'description': project.description,
                'tasks': task_data,
                'completion_percentage': completion_percentage,
                'difficulty_level': project.difficulty_level,
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

        # Check if the answer is correct
        if task.check_answer(chosen_answer):
            # Update or create TaskCompletion entry
            task_completion, created = TaskCompletion.objects.update_or_create(
                user=request.user, 
                task=task,
                defaults={'is_completed': True, 'completed_date': timezone.now()}
            )
            task.mark_as_completed()  # Update project completion status if necessary
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
                level = profile.studentprofile.level if hasattr(profile, 'studentprofile') else 0
                last_seen = profile.last_seen
            except Profile.DoesNotExist:
                online_status = False
                level = 0
                last_seen = None
            users_data.append({
                "username": user.username,
                "level": level,
                "online": online_status,
            })

        return Response(users_data)

class ProfileDetailAPIView(APIView):
    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            if profile.role == 'student':
                student_profile = StudentProfile.objects.get(profile=profile)
                serializer = StudentProfileSerializer(student_profile)
            elif profile.role == 'teacher':
                teacher_profile = TeacherProfile.objects.get(profile=profile)
                serializer = TeacherProfileSerializer(teacher_profile)
            else:
                serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        data = request.data

        # Handle updating User fields (username, email, password)
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)

        password = data.get('password', None)
        if password:
            try:
                validate_password(password, user)
                user.set_password(password)
            except ValidationError as e:
                return Response({"password": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        user.save()

        # Handle updating Profile fields
        profile = user.profile
        profile_serializer = ProfileSerializer(profile, data=data, partial=True)
        if profile_serializer.is_valid():
            profile_serializer.save()

            if profile.role == 'student':
                student_profile = profile.studentprofile
                student_serializer = StudentProfileSerializer(student_profile, data=data, partial=True)
                if student_serializer.is_valid():
                    student_serializer.save()
            elif profile.role == 'teacher':
                teacher_profile = profile.teacherprofile
                teacher_serializer = TeacherProfileSerializer(teacher_profile, data=data, partial=True)
                if teacher_serializer.is_valid():
                    teacher_serializer.save()

            return Response(profile_serializer.data)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


