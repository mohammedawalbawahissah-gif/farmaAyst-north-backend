from django.utils import timezone
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Disbursement, RepaymentSchedule, Payment
from .serializers import (DisbursementSerializer, RepaymentScheduleSerializer,
                          PaymentSerializer, InitiateRepaymentSerializer)
from .services import momo_service, paystack_service
from accounts.permissions import IsAdmin, IsFarmer
from notifications.utils import send_notification


class RepaymentScheduleViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RepaymentScheduleSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'farmer':
            return RepaymentSchedule.objects.filter(agreement__farmer=user)
        if user.role == 'investor':
            return RepaymentSchedule.objects.filter(agreement__investor=user)
        if user.role == 'admin':
            return RepaymentSchedule.objects.all()
        return RepaymentSchedule.objects.none()


class InitiateRepaymentView(generics.GenericAPIView):
    serializer_class = InitiateRepaymentSerializer
    permission_classes = [IsFarmer]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        schedule = RepaymentSchedule.objects.get(
            id=data['schedule_id'],
            agreement__farmer=request.user
        )

        payment = Payment.objects.create(
            payer=request.user,
            payment_type='repayment',
            amount=schedule.amount_due,
            method=data['method'],
            schedule=schedule,
            phone_number=data.get('phone_number', ''),
        )

        if data['method'] == 'momo':
            result = momo_service.request_to_pay(
                amount=str(schedule.amount_due),
                phone=data.get('phone_number', ''),
                reference=payment.reference,
                narration=f'FarmAsyst North repayment — {schedule.agreement.reference}'
            )
            payment.gateway_ref = result.get('reference_id', '')
            payment.gateway_response = result
            if result.get('success'):
                payment.status = 'pending'
                send_notification(request.user, 'repayment_due',
                                  'Repayment Initiated',
                                  f'GHS {schedule.amount_due} repayment initiated via MoMo.')
            else:
                payment.status = 'failed'
            payment.save()

        elif data['method'] == 'paystack':
            result = paystack_service.initialize_transaction(
                email=request.user.email,
                amount_ghs=float(schedule.amount_due),
                reference=payment.reference,
            )
            payment.gateway_response = result
            payment.save()
            if result.get('success'):
                return Response({
                    'payment': PaymentSerializer(payment).data,
                    'authorization_url': result['data'].get('authorization_url'),
                })

        return Response(PaymentSerializer(payment).data)


class PaystackWebhookView(generics.GenericAPIView):
    permission_classes = []

    def post(self, request):
        event = request.data.get('event')
        data  = request.data.get('data', {})
        if event == 'charge.success':
            ref = data.get('reference', '')
            try:
                payment = Payment.objects.get(reference=ref)
                payment.status = 'success'
                payment.updated_at = timezone.now()
                payment.save()
                if payment.schedule:
                    payment.schedule.amount_paid = payment.amount
                    payment.schedule.status = 'paid'
                    payment.schedule.paid_at = timezone.now()
                    payment.schedule.save()
                send_notification(payment.payer, 'repayment_received',
                                  'Repayment Confirmed ✅',
                                  f'GHS {payment.amount} payment received.')
            except Payment.DoesNotExist:
                pass
        return Response({'status': 'ok'})


class DisbursementViewSet(viewsets.ModelViewSet):
    serializer_class = DisbursementSerializer
    permission_classes = [IsAdmin]
    queryset = Disbursement.objects.all()

    def perform_create(self, serializer):
        disbursement = serializer.save(disbursed_by=self.request.user)
        # Trigger MoMo transfer
        agreement = disbursement.agreement
        farmer = agreement.farmer
        result = momo_service.transfer(
            amount=str(disbursement.amount),
            phone=farmer.phone,
            reference=disbursement.reference,
            narration=f'FarmAsyst North disbursement — {agreement.reference}',
        )
        disbursement.gateway_ref = result.get('reference_id', '')
        disbursement.gateway_response = result
        disbursement.status = 'processing' if result.get('success') else 'failed'
        disbursement.save()
        if result.get('success'):
            send_notification(farmer, 'disbursement',
                              'Funds Disbursed 🎉',
                              f'GHS {disbursement.amount} has been sent to your MoMo.')
