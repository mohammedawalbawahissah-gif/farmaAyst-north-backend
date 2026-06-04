from rest_framework import serializers
from .models import Farm, FarmActivityLog, FarmAuditReport


class FarmSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)

    class Meta:
        model = Farm
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class FarmActivityLogSerializer(serializers.ModelSerializer):
    flock_count = serializers.ReadOnlyField()   # computed property: sum of all categories

    class Meta:
        model = FarmActivityLog
        fields = '__all__'
        read_only_fields = ['id', 'logged_by', 'created_at']


class FarmAuditReportSerializer(serializers.ModelSerializer):
    auditor_name = serializers.SerializerMethodField()
    farm_name    = serializers.CharField(source='farm.name', read_only=True)

    class Meta:
        model = FarmAuditReport
        fields = '__all__'
        read_only_fields = ['id', 'auditor', 'created_at']

    def get_auditor_name(self, obj):
        if obj.auditor:
            return obj.auditor.get_full_name()
        return None
