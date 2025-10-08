from rest_framework import serializers
from .models import Profile, Project, Leaves

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
