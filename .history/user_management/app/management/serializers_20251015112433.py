from rest_framework import serializers
from .models import WorkTiming, User
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from app.project.models import Project
from app.leaves.models import Leaves
from app.task.models import Task

User = get_user_model()


class ActiveProjectListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        # Filter the queryset before serializing the list of objects
        data = data.filter(is_deleted=False) 
        return super().to_representation(data)

class ProjectNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'status', 'start_date', 'end_date']
        list_serializer_class = ActiveProjectListSerializer

class ActiveLeavesListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(is_deleted=False)
        return super().to_representation(data)

class LeavesNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaves
        fields = ['id', 'leave_type', 'start_date', 'end_date', 'approved_status', 'reason']
        list_serializer_class = ActiveLeavesListSerializer

class ActiveWorkTimingListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(is_deleted=False)
        return super().to_representation(data)

class WorkTimingNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkTiming
        fields = ['id', 'date', 'clock_in', 'clock_out']
        list_serializer_class = ActiveWorkTimingListSerializer

class ActiveTaskListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        data = data.filter(is_deleted=False)
        return super().to_representation(data)

class TaskNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'project', 'assigned_to', 'title', 'description', 'status', 'priority', 'due_date']
        list_serializer_class = ActiveTaskListSerializer


class UserSignupSerializer(serializers.ModelSerializer):
    def validate_email(self, value):  
        matching_users = User.objects.filter(email__iexact=value)
        if self.instance:
            if matching_users.filter(pk=self.instance.pk).exists():
                return value
            if matching_users.exists():
                raise serializers.ValidationError("This email address is already registered.")
        elif matching_users.exists():
            raise serializers.ValidationError("This email address is already registered.")
        return value 
    
    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)
        if 'email' in internal_value:
            internal_value['email'] = internal_value['email'].lower()
        return internal_value
    
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
    access = serializers.CharField()
    refresh = serializers.CharField()


class WorkTimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkTiming
        fields = '__all__'
        read_only_fields = ['user', 'is_deleted', 'created_by', 'updated_by']

class UserDetailSerializer(serializers.ModelSerializer):
    projects = ProjectNestedSerializer(many=True, read_only=True)
    leaves = LeavesNestedSerializer(many=True, read_only=True, source='leaves_set')
    worktimings = WorkTimingNestedSerializer(many=True, read_only=True, source='worktiming_set')
    tasks = TaskNestedSerializer(many=True, read_only=True, source='tasks_assigned')

    class Meta:
        model = User
        fields = [
            'id', 'name', 'email', 'number', 'age', 'gender', 'is_staff', 
            'projects', 'leaves', 'worktimings', 'tasks',
        ]
