from rest_framework import serializers
from .models import Farm, FarmActivityLog, FarmAuditReport


class FarmSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)

    class Meta:
        model = Farm
        fields = '__all__'
        read_only_fields = ['id', 'owner', 'created_at', 'updated_at']


class FarmActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmActivityLog
        fields = '__all__'
        read_only_fields = ['id', 'logged_by', 'created_at']


class FarmAuditReportSerializer(serializers.ModelSerializer):
    auditor_name = serializers.CharField(source='auditor.get_full_name', read_only=True)

    class Meta:
        model = FarmAuditReport
        fields = '__all__'
        read_only_fields = ['id', 'auditor', 'created_at']
