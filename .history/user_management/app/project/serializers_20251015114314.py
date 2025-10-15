from rest_framework import serializers
from .models import  Project

class ProjectSerializer(serializers.ModelSerializer):

    def validate(self, data):
        
        start_date = data.get('start_date')
        end_date = data.get('end_date')

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
