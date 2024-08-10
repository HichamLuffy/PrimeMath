from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import User, Courses, Projects


# Create your views here.
def main(request, id):
    course1 = Courses.objects.get(id=id)
    return HttpResponse("PrimeMath %s" %course1.name)
    #return render(request, 'main.html')


def Login(request):
    return HttpResponse("SignUp")
    #return render(request, 'main.html')

def Register(request):
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