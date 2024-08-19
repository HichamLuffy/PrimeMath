from rest_framework import serializers
from .models import Profile, Courses, StudentProfile, TeacherProfile
from django.contrib.auth.models import User



class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'
        extra_kwargs = {'teacher_owner': {'read_only': True}}

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'role', 'age', 'current_study', 'status', 'teaching_experience', 'subjects_of_expertise', 'certifications']

    def create(self, validated_data):
        user = validated_data['user']
        role = validated_data['role']
        
        # Create Profile with the provided role
        profile = Profile.objects.create(user=user, role=role)

        # Automatically create the role-based profile
        if role == 'student':
            StudentProfile.objects.create(profile=profile)
        elif role == 'teacher':
            TeacherProfile.objects.create(profile=profile)
        
        return profile

class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'profile']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
