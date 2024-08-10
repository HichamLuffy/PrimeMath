from django.contrib import admin
from .models import Courses, Student, Teacher, Projects, Tasks, StudentCourseEnrollment

#TODO Register your models here.

admin.site.register(Courses)
admin.site.register(StudentCourseEnrollment)
admin.site.register(Projects)
admin.site.register(Tasks)
admin.site.register(Teacher)
admin.site.register(Student)