from rest_framework import serializers
from .models import WorkTiming, User
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from project.models import Project
from leaves.models import Leaves

User = get_user_model()

class ProjectNested



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


