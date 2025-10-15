from rest_framework import serializers
from .models import Leaves
from django

class LeavesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaves
        fields = [
            'id', 'leave_type', 'start_date', 'end_date', 'reason', 
            'approved_status', 
            'is_deleted', 'created_by', 'updated_by',
        ]        
        read_only_fields = ['user', 'created_by', 'updated_by', 'is_deleted']