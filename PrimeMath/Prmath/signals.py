from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, StudentProfile, TeacherProfile

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         # profile = Profile.objects.create(user=instance)
#         # if profile.role == 'student':
#         #     StudentProfile.objects.create(profile=profile)
#         # elif profile.role == 'teacher':
#         #     TeacherProfile.objects.create(profile=profile)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()