from django.db import models
from django.contrib.auth.models import User

# User model is already provided by Django, no need to redefine it.
class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10)  # "student" or "teacher"
    age = models.IntegerField(null=True, blank=True)
    current_study = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)  # For teachers
    teaching_experience = models.IntegerField(null=True, blank=True)  # Years of experience
    subjects_of_expertise = models.ManyToManyField(Subject, blank=True)  # Expertise in subjects
    certifications = models.TextField(null=True, blank=True)  # Certifications or qualifications

    def __str__(self):
        return self.user.username



class Courses(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    teacher_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    featured_order = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)  # Default should be False
    is_locked = models.BooleanField(default=False)
    lock_reason = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    number_of_students_in_course = models.PositiveIntegerField(default=0)
    number_of_students_completed = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    def update_completion_status(self):
        """Updates the completion status of the course based on project completions."""
        total_projects = self.projects_set.count()
        completed_projects = self.projects_set.filter(is_completed=True).count()
        if total_projects > 0 and (completed_projects / total_projects) >= 0.7:
            self.is_completed = True
        else:
            self.is_completed = False
        self.save()
    
    def update_enrollment_status(self):
        """Updates the enrollment status of the course based on student enrollments."""
        total_students = self.studentcourseenrollment_set.count()
        completed_students = self.studentcourseenrollment_set.filter(completed_date__isnull=False).count()
        if total_students > 0 and (completed_students / total_students) >= 0.7:
            self.is_locked = True
        else:
            self.is_locked = False
        self.save()

class StudentCourseEnrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    progress = models.PositiveIntegerField(default=0)  # Percentage completion
    grade = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.name}"


class Projects(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    teacher_owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, limit_choices_to={'role': 'teacher'})
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)
    difficulty_level = models.PositiveIntegerField(default=1)
    current_students = models.PositiveIntegerField(default=0)
    number_of_students_completed = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_locked = models.BooleanField(default=False)
    lock_reason = models.CharField(max_length=200, blank=True)
    help_links = models.TextField(blank=True)  # Could store links in a comma-separated format

    def __str__(self):
        return self.title

    def update_completion_status(self):
        """Updates the completion status of the project based on task completions."""
        total_tasks = self.tasks_set.count()
        completed_tasks = self.tasks_set.filter(is_completed=True).count()
        if total_tasks > 0 and (completed_tasks / total_tasks) >= 0.6:
            self.is_completed = True
        else:
            self.is_completed = False
        self.save()


class Tasks(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)
    difficulty_level = models.PositiveIntegerField(default=1)
    question = models.TextField()  # The question associated with the task
    options = models.JSONField()  # Store options as JSON, e.g., {"A": "Option 1", "B": "Option 2"}
    correct_answer = models.CharField(max_length=200)  # The correct option
    chosen_answer = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

    def check_answer(self):
        """Check if the chosen answer is correct and mark the task as completed."""
        if self.chosen_answer == self.correct_answer:
            self.is_completed = True
            self.completed_date = models.DateTimeField(auto_now=True)
        else:
            self.is_completed = False
        self.save()
        self.project.update_completion_status()  # Update project status after task is checked
