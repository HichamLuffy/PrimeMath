from django.contrib import admin
from .models import Courses, Subject, Profile, Projects, Tasks, StudentCourseEnrollment

#TODO Register your models here.

admin.site.register(Courses)
admin.site.register(StudentCourseEnrollment)
admin.site.register(Projects)
admin.site.register(Tasks)
admin.site.register(Profile)
admin.site.register(Subject)