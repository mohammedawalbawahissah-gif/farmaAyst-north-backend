from rest_framework import serializers
from .models import CreditApplication, ApplicationDocument, CreditAgreement
from accounts.serializers import UserSerializer
from farms.models import Farm


class ApplicationDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationDocument
        fields = ['id', 'doc_type', 'file', 'original_name', 'uploaded_at']
        read_only_fields = ['uploaded_at']


class CreditApplicationSerializer(serializers.ModelSerializer):
    farmer_name = serializers.CharField(source='farmer.get_full_name', read_only=True)
    documents   = ApplicationDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = CreditApplication
        fields = ['id', 'reference', 'farmer', 'farmer_name', 'farm', 'credit_type',
                  'amount_requested', 'repayment_period_months', 'purpose', 'input_details',
                  'status', 'credit_score_at_submission', 'reviewer', 'reviewer_notes',
                  'rejection_reason', 'submitted_at', 'reviewed_at', 'approved_at',
                  'created_at', 'updated_at', 'documents']
        read_only_fields = ['id', 'reference', 'farmer', 'status', 'credit_score_at_submission',
                            'reviewer', 'reviewer_notes', 'rejection_reason',
                            'submitted_at', 'reviewed_at', 'approved_at', 'created_at', 'updated_at']


class CreditApplicationAdminSerializer(CreditApplicationSerializer):
    farmer = UserSerializer(read_only=True)

    class Meta(CreditApplicationSerializer.Meta):
        read_only_fields = ['id', 'reference', 'created_at', 'updated_at']


class CreditAgreementSerializer(serializers.ModelSerializer):
    farmer_name   = serializers.CharField(source='farmer.get_full_name', read_only=True)
    investor_name = serializers.CharField(source='investor.get_full_name', read_only=True)

    class Meta:
        model = CreditAgreement
        fields = '__all__'
        read_only_fields = ['id', 'reference', 'farmer_signed_at', 'investor_signed_at',
                            'created_at', 'updated_at']
