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
        print(f"Validated data: {validated_data}")  # Debugging line
        user = validated_data['user']
        role = validated_data['role']

        # Create Profile with the provided role
        profile = Profile.objects.create(user=user, role=role)
        print(f"Profile created for user {user.username} with role {role}")  # Debugging line

        # Automatically create the role-based profile
        if role == 'student':
            StudentProfile.objects.create(profile=profile)
            print(f"StudentProfile created for user {user.username}")  # Debugging line
        elif role == 'teacher':
            TeacherProfile.objects.create(profile=profile)
            print(f"TeacherProfile created for user {user.username}")  # Debugging line
        
        return profile

class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'profile']

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(write_only=True, required=False)  # Accept role name

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        role = validated_data.pop('role', 'student')  # Default to 'student' if no role provided
        user = User.objects.create_user(**validated_data)
        
        return user