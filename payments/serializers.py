from rest_framework import serializers
from .models import Disbursement, RepaymentSchedule, Payment


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
