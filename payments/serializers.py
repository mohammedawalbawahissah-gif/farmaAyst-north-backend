from rest_framework import serializers
from .models import Disbursement, RepaymentSchedule, Payment, DisbursementRequest


class DisbursementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disbursement
        fields = '__all__'
        read_only_fields = ['id', 'reference', 'disbursed_by', 'gateway_ref',
                            'gateway_response', 'processed_at', 'created_at']


class RepaymentScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepaymentSchedule
        fields = '__all__'
        read_only_fields = ['id', 'amount_paid', 'status', 'paid_at']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['id', 'reference', 'payer', 'status', 'gateway_ref',
                            'gateway_response', 'created_at', 'updated_at']


class InitiateRepaymentSerializer(serializers.Serializer):
    schedule_id  = serializers.UUIDField()
    method       = serializers.ChoiceField(choices=['momo', 'paystack'])
    phone_number = serializers.CharField(required=False)


class DisbursementRequestSerializer(serializers.ModelSerializer):
    requested_by_name = serializers.SerializerMethodField()
    reviewed_by_name  = serializers.SerializerMethodField()
    farmer_name       = serializers.SerializerMethodField()
    agreement_reference = serializers.SerializerMethodField()

    class Meta:
        model = DisbursementRequest
        fields = '__all__'
        read_only_fields = [
            'id', 'reference', 'requested_by', 'amount', 'status',
            'reviewed_by', 'reviewed_at', 'disbursement', 'created_at', 'updated_at',
        ]

    def get_requested_by_name(self, obj):
        return obj.requested_by.get_full_name() or obj.requested_by.email

    def get_reviewed_by_name(self, obj):
        if obj.reviewed_by:
            return obj.reviewed_by.get_full_name() or obj.reviewed_by.email
        return None

    def get_farmer_name(self, obj):
        return obj.agreement.farmer.get_full_name() or obj.agreement.farmer.email

    def get_agreement_reference(self, obj):
        return obj.agreement.reference


class PayFullBalanceSerializer(serializers.Serializer):
    agreement_id = serializers.UUIDField()
    method       = serializers.ChoiceField(choices=['momo', 'paystack'])
    phone_number = serializers.CharField(required=False)


class ApproveDisbursementSerializer(serializers.Serializer):
    method = serializers.ChoiceField(choices=['momo', 'paystack', 'cash', 'in_kind'])
    notes  = serializers.CharField(required=False, allow_blank=True)


class RejectDisbursementSerializer(serializers.Serializer):
    reason = serializers.CharField()
