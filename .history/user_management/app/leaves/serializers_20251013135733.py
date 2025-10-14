from rest_framework import serializers
from .models import Leaves

class LeavesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaves
        fields = '__all__'
        read_only_fields = ['user', '''created_by', 'updated_by', 'is_deleted']