from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Farm, FarmActivityLog, FarmAuditReport
from .serializers import FarmSerializer, FarmActivityLogSerializer, FarmAuditReportSerializer
from accounts.permissions import (IsFarmer, IsAdmin, IsFarmerOrAdmin,
                                   IsMonitoringOfficerOrAdmin, IsMonitoringOfficer)


class FarmViewSet(viewsets.ModelViewSet):
    serializer_class = FarmSerializer
    filter_backends  = [DjangoFilterBackend]
    filterset_fields = ['flock_type', 'region', 'district', 'is_active']
    search_fields    = ['name', 'region', 'district', 'community']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'farmer':
            return Farm.objects.filter(owner=user)
        if user.role in ('admin', 'investor', 'monitoring_officer'):
            return Farm.objects.all()
        return Farm.objects.none()

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [IsFarmer()]
        if self.action == 'create':
            return [IsFarmerOrAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == 'admin':
            owner_id = self.request.data.get('owner')
            if not owner_id:
                from rest_framework.exceptions import ValidationError
                raise ValidationError({'owner': 'This field is required when registering a farm as admin.'})
            from accounts.models import User as UserModel
            try:
                owner = UserModel.objects.get(id=owner_id, role='farmer')
            except UserModel.DoesNotExist:
                from rest_framework.exceptions import ValidationError
                raise ValidationError({'owner': 'No farmer account found with that ID.'})
            serializer.save(owner=owner)
        else:
            serializer.save(owner=user)


class FarmActivityLogViewSet(viewsets.ModelViewSet):
    serializer_class = FarmActivityLogSerializer
    filter_backends  = [DjangoFilterBackend]
    filterset_fields = ['farm', 'date']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'farmer':
            return FarmActivityLog.objects.filter(farm__owner=user)
        if user.role in ('admin', 'monitoring_officer'):
            return FarmActivityLog.objects.all()
        return FarmActivityLog.objects.none()

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update'):
            return [IsFarmer()]
        return [IsFarmerOrAdmin()]

    def perform_create(self, serializer):
        serializer.save(logged_by=self.request.user)


class FarmAuditReportViewSet(viewsets.ModelViewSet):
    serializer_class = FarmAuditReportSerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == 'farmer':
            return FarmAuditReport.objects.filter(farm__owner=user)
        if user.role == 'monitoring_officer':
            # Officers see all reports but can only edit their own
            return FarmAuditReport.objects.select_related('farm', 'auditor').all()
        if user.role in ('admin', 'investor'):
            return FarmAuditReport.objects.select_related('farm', 'auditor').all()
        return FarmAuditReport.objects.none()

    def get_permissions(self):
        if self.action == 'create':
            # Both monitoring officers and admins can submit audit reports
            return [IsMonitoringOfficerOrAdmin()]
        if self.action in ('update', 'partial_update'):
            # Officers can only update; admins can do anything
            return [IsMonitoringOfficerOrAdmin()]
        if self.action == 'destroy':
            return [IsAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(auditor=self.request.user)

    def perform_update(self, serializer):
        user = self.request.user
        # Monitoring officers can only edit reports they themselves submitted
        if user.role == 'monitoring_officer':
            instance = self.get_object()
            if instance.auditor != user:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied('You can only edit audit reports you submitted.')
        serializer.save()
