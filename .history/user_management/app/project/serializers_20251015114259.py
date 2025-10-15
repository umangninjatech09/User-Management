from rest_framework import serializers
from .models import  Project

class ProjectSerializer(serializers.ModelSerializer):

    def validate(self, data):
        """
        Check that the end_date is not before the start_date.
        """
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        # Check if both dates are present (they might be missing if partial=True 
        # is used and only one is submitted, but for creation both should be there).
        # We assume dates are already Python date objects here due to field type handling.
        
        if start_date and end_date:
            if end_date < start_date:
                raise serializers.ValidationError(
                    {"end_date": "The end date cannot be before the start date."}
                )
        
        # If the instance exists (update), handle cases where one date might be missing
        # but the other is being updated.
        if self.instance:
            # Use data.get(field) if new value exists, otherwise use self.instance.field
            start_date = data.get('start_date', self.instance.start_date)
            end_date = data.get('end_date', self.instance.end_date)
            
            if end_date < start_date:
                raise serializers.ValidationError(
                    {"end_date": "The end date cannot be before the start date."}
                )


        return data
    class Meta:
        model = Project
        fields = '__all__'
