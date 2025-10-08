from rest_framework import serializers
from .models import WorkTiming, User
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from project.models import Project
from leaves.models import Leaves

User = get_user_model()

class ProjectNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'status', 'start_date', 'end_date']

class LeavesNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaves
        fields = ['id', 'leave_type', 'start_date', 'end_date', 'approved_status', 'reason']

class WorkTimingNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkTiming
        fields = ['id', 'date', 'clock_in', 'clock_out']


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


class WorkTimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkTiming
        fields = '__all__'

class UserDetailSerializer(serializers.ModelSerializer):
    projects = ProjectNestedSerializer(many=True, read_only=True)
    


