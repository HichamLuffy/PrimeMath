from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.shortcuts import HttpResponse
from django.contrib import messages
from .models import User, Courses, Projects, Profile
from .decorators import student_required, teacher_required

# Create your views here.

@student_required
def student_dashboard(request):
    return HttpResponse("PrimeMath teacher")
    #return render(request, 'main.html')

@teacher_required
def teacher_dashboard(request):
    return HttpResponse("PrimeMath student")
    #return render(request, 'main.html')


def Login(request):

    return HttpResponse("SignUp")
    #return render(request, 'main.html')

def Register(request):
    if request.method == 'POST':
        username = request.Post['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        role = request.POST['role']
        if password1 == password2:
            if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                messages.error(request, 'Username or email already exists')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()

                user_model = User.objects.get(username=username)
                if role == 'student':
                    age = request.POST['age']
                    current_study = request['current_study']
                    new_profile = Profile.objects.create(user=user_model, role='student', age=age, current_study=current_study)
                elif role == 'teacher':
                    status = request.POST['status'] # Real teacher, degree holder, etc.
                    teaching_experience = request.POST['teaching_experience']
                    subjects_of_expertise = request.POST.getlist('subjects_of_expertise')
                    certifications = request.POST['certifications']
                    new_profile = Profile.objects.create(user=user_model, role='teacher', status = status, teaching_experience = teaching_experience, subjects_of_expertise = subjects_of_expertise, certifications = certifications)
                new_profile.save()
                messages.success(request, 'Registration successful')
                return redirect('login')
    return HttpResponse("Register")
    #return render(request, 'main.html')

def Courses_page(request):
    return HttpResponse("courses")
    #return render(request, 'main.html')

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