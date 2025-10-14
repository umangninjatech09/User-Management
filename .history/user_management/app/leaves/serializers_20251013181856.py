from rest_framework import serializers
from .models import Leaves

class LeavesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaves
        fields = [
            'id', 'leave_type', 'start_date', 'end_date', 'reason', 
            # ✅ ENSURE 'approved_status' is included here
            'approved_status', 
            'is_deleted', 'created_by', 'updated_by', 'created_at', 'updated_at'
        ]        
        read_only_fields = ['user', 'approved_status','created_by', 'updated_by', 'is_deleted']