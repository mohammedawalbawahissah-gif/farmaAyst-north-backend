from django.utils import timezone
from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import CreditApplication, ApplicationDocument, CreditAgreement
from .serializers import (CreditApplicationSerializer, CreditApplicationAdminSerializer,
                          ApplicationDocumentSerializer, CreditAgreementSerializer)
from accounts.permissions import IsFarmer, IsAdmin, IsInvestorOrAdmin, IsFarmerOrAdmin
from notifications.utils import send_notification


class CreditApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = CreditApplicationSerializer
    filter_backends  = [DjangoFilterBackend]
    filterset_fields = ['status', 'credit_type']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'farmer':
            return CreditApplication.objects.filter(farmer=user)
        if user.role == 'admin':
            return CreditApplication.objects.all()
        return CreditApplication.objects.none()

    def get_serializer_class(self):
        if self.request.user.role == 'admin':
            return CreditApplicationAdminSerializer
        return CreditApplicationSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update'):
            return [IsFarmer()]
        return [IsFarmerOrAdmin()]

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsFarmer])
    def submit(self, request, pk=None):
        app = self.get_object()
        if app.status != 'draft':
            return Response({'detail': 'Only draft applications can be submitted.'}, status=400)
        app.status = 'submitted'
        app.submitted_at = timezone.now()
        app.credit_score_at_submission = request.user.farmer_profile.credit_score if hasattr(request.user, 'farmer_profile') else 0
        app.save()
        send_notification(app.farmer, 'application_status',
                          'Application Submitted',
                          f'Your application {app.reference} has been submitted for review.')
        return Response(CreditApplicationSerializer(app).data)

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def approve(self, request, pk=None):
        app = self.get_object()
        app.status = 'approved'
        app.reviewer = request.user
        app.reviewer_notes = request.data.get('notes', '')
        app.reviewed_at = timezone.now()
        app.approved_at = timezone.now()
        app.save()
        send_notification(app.farmer, 'application_status',
                          'Application Approved 🎉',
                          f'Your application {app.reference} has been approved.')
        return Response(CreditApplicationAdminSerializer(app).data)

    @action(detail=True, methods=['post'], permission_classes=[IsAdmin])
    def reject(self, request, pk=None):
        app = self.get_object()
        app.status = 'rejected'
        app.reviewer = request.user
        app.reviewer_notes = request.data.get('notes', '')
        app.rejection_reason = request.data.get('reason', '')
        app.reviewed_at = timezone.now()
        app.save()
        send_notification(app.farmer, 'application_status',
                          'Application Not Approved',
                          f'Your application {app.reference} was not approved. Reason: {app.rejection_reason}')
        return Response(CreditApplicationAdminSerializer(app).data)


class DocumentUploadView(generics.CreateAPIView):
    serializer_class = ApplicationDocumentSerializer
    permission_classes = [IsFarmer]

    def perform_create(self, serializer):
        app_id = self.kwargs['application_id']
        app = CreditApplication.objects.get(id=app_id, farmer=self.request.user)
        file = self.request.FILES.get('file')
        serializer.save(application=app, original_name=file.name if file else '')


class CreditAgreementViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CreditAgreementSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'farmer':
            return CreditAgreement.objects.filter(farmer=user)
        if user.role == 'investor':
            return CreditAgreement.objects.filter(investor=user)
        if user.role == 'admin':
            return CreditAgreement.objects.all()
        return CreditAgreement.objects.none()

    @action(detail=True, methods=['post'])
    def sign(self, request, pk=None):
        agreement = self.get_object()
        user = request.user
        now = timezone.now()
        if user.role == 'farmer' and agreement.farmer == user:
            agreement.farmer_signed_at = now
        elif user.role == 'investor' and agreement.investor == user:
            agreement.investor_signed_at = now
        else:
            return Response({'detail': 'Not authorised to sign this contract.'}, status=403)
        if agreement.farmer_signed_at and agreement.investor_signed_at:
            agreement.status = 'active'
        agreement.save()
        return Response(CreditAgreementSerializer(agreement).data)
