from rest_framework import serializers
from .models import Leaves

class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = [
            'id', 'leave_type', 'start_date', 'end_date', 'reason', 
            # ✅ ENSURE 'approved_status' is included here
            'approved_status', 
            'is_deleted', 'created_by', 'updated_by', 'created_at', 'updated_at'
        ]
        
        # ✅ Ensure 'approved_status' is NOT in the read_only_fields
        read_only_fields = ['created_at', 'updated_at', 'created_by', 'updated_by'] 
        
        # ✅ Also ensure it's not excluded in extra_kwargs (less common)
        # extra_kwargs = {'approved_status': {'write_only': False}} 