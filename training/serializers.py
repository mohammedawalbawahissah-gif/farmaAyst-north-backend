from rest_framework import serializers
from .models import TrainingModule, TrainingEnrolment


class TrainingModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingModule
        fields = '__all__'
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']


class TrainingEnrolmentSerializer(serializers.ModelSerializer):
    module_title = serializers.CharField(source='module.title', read_only=True)

    class Meta:
        model = TrainingEnrolment
        fields = '__all__'
        read_only_fields = ['id', 'farmer', 'enrolled_at', 'completed_at']
