from rest_framework import serializers
from .models import Profile, Courses, StudentProfile, TeacherProfile, Subject
from django.contrib.auth.models import User



class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'
        extra_kwargs = {'teacher_owner': {'read_only': True}}

class ProfileSerializer(serializers.ModelSerializer):
    subjects_of_expertise = serializers.SlugRelatedField(slug_field='name', queryset=Subject.objects.all(), many=True)

    class Meta:
        model = Profile
        fields = ['user', 'role', 'age', 'current_study', 'status', 'teaching_experience', 'subjects_of_expertise', 'certifications']

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
        role = validated_data.pop('role', 'student')
        user = User.objects.create_user(**validated_data)
        
        # Create Profile with the provided role
        profile = Profile.objects.create(user=user, role=role)

        # Automatically create the role-based profile
        if role == 'student':
            StudentProfile.objects.create(profile=profile)
        elif role == 'teacher':
            TeacherProfile.objects.create(profile=profile)
        
        return user