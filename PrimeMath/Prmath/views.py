from django.shortcuts import render
from django.shortcuts import HttpResponse


# Create your views here.
def main(request):
    return HttpResponse("PrimeMath")
    #return render(request, 'main.html')


def Login(request):
    return HttpResponse("SignUp")
    #return render(request, 'main.html')

def Register(request):
    return HttpResponse("Register")
    #return render(request, 'main.html')

def Courses(request):
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