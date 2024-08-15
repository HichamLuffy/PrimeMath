from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
from django.contrib import messages
from .models import User, Courses, Projects, Profile
from .decorators import student_required, teacher_required
from django.contrib.auth import authenticate, login as django_login
from .serializers import ProfileSerializer, UserSerializer, CoursesSerializer
from rest_framework import status, generics
from rest_framework.decorators import api_view
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

    def get_queryset(self):
        user = self.request.user
        return Courses.objects.filter(teacher_owner=user)

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
    

@student_required
def student_dashboard(request):
    return HttpResponse("PrimeMath teacher")
    #return render(request, 'main.html')

@teacher_required
def teacher_dashboard(request):
    return HttpResponse("PrimeMath student")
    #return render(request, 'main.html')


@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        username = request.data['username']
        email = request.data['email']
        password1 = request.data['password1']
        password2 = request.data['password2']
        role = request.data['role']

        if password1 == password2:
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                return Response({'error': 'Username or email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()

                if role == 'student':
                    age = request.data['age']
                    current_study = request.data['current_study']
                    new_profile = Profile.objects.create(user=user, role='student', age=age, current_study=current_study)
                elif role == 'teacher':
                    status = request.data['status']
                    teaching_experience = request.data['teaching_experience']
                    certifications = request.data['certifications']
                    new_profile = Profile.objects.create(user=user, role='teacher', status=status, teaching_experience=teaching_experience, certifications=certifications)

                new_profile.save()
                return Response({'success': 'Registration successful'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
    #return render(request, 'main.html')

@api_view(['POST'])
def login_user(request):
    username = request.data['username']
    password = request.data['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        django_login(request, user)
        profile = Profile.objects.get(user=user)
        return Response({'username': user.username, 'role': profile.role}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)




def Dashboard(request):
    return HttpResponse("Dashboard")
    #return render(request, 'main.html')

def Profile(request):
    return HttpResponse("Profile")
    #return render(request, 'main.html')

def Users(request):
    return HttpResponse("Users")
    #return render(request, 'main.html')

def About(request):
    return HttpResponse("About")
    #return render(request, 'main.html')