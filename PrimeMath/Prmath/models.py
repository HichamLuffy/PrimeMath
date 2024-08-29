from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


# User model is already provided by Django, no need to redefine it.
class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=[('student', 'Student'), ('teacher', 'Teacher')])
    age = models.IntegerField(null=True, blank=True)
    current_study = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)  # For teachers
    teaching_experience = models.IntegerField(null=True, blank=True)  # Years of experience
    subjects_of_expertise = models.ManyToManyField(Subject, blank=True)  # Expertise in subjects
    certifications = models.TextField(null=True, blank=True)  # Certifications or qualifications
    last_seen = models.DateTimeField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    social_links = models.JSONField(null=True, blank=True)  # Store links as JSON, e.g., {"linkedin": "https://www.linkedin.com"}

    def __str__(self):
        return self.user.username

    def is_online(self):
        if self.last_seen:
            now = timezone.now()
            online = now - self.last_seen < timedelta(minutes=5)
            print("##########models#######")
            print(f"Profile: {self.user.username} - Now: {now}, Last Seen: {self.last_seen}, Is Online: {online}")
            return online
        print("##########models#######")
        print(f"Profile: {self.user.username} has no last_seen timestamp.")
        print("##########update_last activite#######")
        return False


class Courses(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    helper_links = models.TextField(blank=True)  # Could store links in a comma-separated format
    score = models.PositiveIntegerField(default=0)
    teacher_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_completed = models.BooleanField(default=False)  # Default should be False
    is_locked = models.BooleanField(default=False)
    lock_reason = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=False)
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


class Projects(models.Model):
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    teacher_owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, limit_choices_to={'role': 'teacher'})
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
        completed_tasks = self.tasks_set.filter(is_completed=True).count()
        total_tasks = self.tasks_set.count()
        self.is_completed = completed_tasks == total_tasks
        self.save()


class Tasks(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
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

    def check_answer(self, chosen_answer):
        return self.correct_answer == chosen_answer

    def mark_as_completed(self):
        self.is_completed = True
        self.completed_date = timezone.now()
        self.save()
        self.project.update_completion_status()


class TaskCompletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'task')
    
    def __str__(self):
        return f"{self.user.username} - {self.task.title}"



class StudentProfile(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    current_study = models.CharField(max_length=200, blank=True, null=True)
    current_courses = models.ManyToManyField(Courses, blank=True)
    completed_courses = models.ManyToManyField(Courses, related_name='completed_students', blank=True)
    current_projects = models.ManyToManyField(Projects, blank=True)
    skills = models.ManyToManyField(Subject, related_name='students', blank=True)
    level = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.profile.user.username

    def join_course(self, course):
        """Add a course to the student's current courses if not already enrolled."""
        if not self.current_courses.filter(id=course.id).exists():
            self.current_courses.add(course)
            course.number_of_students_in_course += 1
            course.save()
        else:
            raise ValidationError("You are already enrolled in this course.")

    def complete_course(self, course):
        """Mark the course as completed and move it from current to completed courses."""
        if self.current_courses.filter(id=course.id).exists():
            self.current_courses.remove(course)
            self.completed_courses.add(course)
            course.number_of_students_completed += 1
            course.save()
            
            # Activate the next course if it exists
            next_course = Courses.objects.filter(id=course.id + 1).first()
            if next_course:
                next_course.is_active = True
                next_course.save()
        else:
            raise ValidationError("You are not enrolled in this course.")


class TeacherProfile(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    points = models.PositiveIntegerField(default=0)
    courses_taught = models.ManyToManyField(Courses, related_name='teachers', blank=True)
    projects_created = models.ManyToManyField(Projects, related_name='teachers', blank=True)
    skills = models.ManyToManyField(Subject, related_name='teachers', blank=True)

    def __str__(self):
        return self.profile.user.username