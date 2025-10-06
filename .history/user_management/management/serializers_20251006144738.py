from rest_framework import serializers
from .models import Project, Leaves, WorkTiming, User
from rest_framework_simplejwt.tokens import RefreshToken


# Signup serializer
class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'number', 'age', 'gender']

# Request OTP
class OTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

# Verify OTP
class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

# JWT Token response
class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class LeavesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaves
        fields = '__all__'
        read_only_fields = ['created_by', 'updated_by', 'is_deleted']


class WorkTimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkTiming
        fields = '__all__'
