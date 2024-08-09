from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class User(models.Model):


class Courses(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    featured_order = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=True)
    is_locked = models.BooleanField(default=False)
    lock_reason = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    number_of_students_in_course = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

class StudentCourseEnrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    progress = models.PositiveIntegerField(default=0)  # Could represent percentage completion
    grade = models.CharField(max_length=10, blank=True)


class Projects(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    difficulty_level = models.PositiveIntegerField(default=1)
    current_students = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_locked = models.BooleanField(default=False)
    lock_reason = models.CharField(max_length=200, blank=True)
    number_of_students_in_project = models.PositiveIntegerField(default=0)

class Tasks(models.Model):
    