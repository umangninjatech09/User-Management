from rest_framework import serializers
from .models import Leaves
from django.utils import timezone

class LeavesSerializer(serializers.ModelSerializer):
    def validate(self, data):
        """
        Check that the end_date is not before the start_date.
        """
        # Get dates from incoming data or use existing instance values for updates
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        # --- Handling Partial Updates (PUT/PATCH) ---
        # If the serializer is updating an existing instance:
        if self.instance:
            # Use data if provided, otherwise use the existing instance value
            start_date = start_date if start_date is not None else self.instance.start_date
            end_date = end_date if end_date is not None else self.instance.end_date
            
        # --- Cross-Field Validation ---
        if start_date and end_date:
            # All dates should be handled as date objects by ModelSerializer, 
            # allowing direct comparison.
            if end_date < start_date:
                raise serializers.ValidationError(
                    {"end_date": "The end date for the leave cannot be before the start date."}
                )
        
        # Ensure that if the start_date is set, it's not in the past (common leave rule)
        if start_date and start_date < timezone.now().date():
             # You may choose to enforce this:
             # raise serializers.ValidationError(
             #    {"start_date": "Leave start date cannot be in the past."}
             # )
            pass # Skipping this past date check for now

        return data


    class Meta:
        model = Leaves
        fields = [
            'id', 'leave_type', 'start_date', 'end_date', 'reason', 
            'approved_status', 
            'is_deleted', 'created_by', 'updated_by',
        ] 
        read_only_fields = ['user', 'created_by', 'updated_by', 'is_deleted']