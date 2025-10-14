from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    assigned_user = serializers.CharField(source='assigned_to.email', read_only=True)

    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'status', 'priority',
            'project', 'project_name', 'assigned_to', 'assigned_user',
            'created_at', 'updated_at', 'due_date'
        ]

        read_only_fields = ['is_deleted', 'created_by', 'updated_by', '']
