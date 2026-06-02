from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Farm, FarmActivityLog, FarmAuditReport
from .serializers import FarmSerializer, FarmActivityLogSerializer, FarmAuditReportSerializer
from accounts.permissions import IsFarmer, IsAdmin, IsFarmerOrAdmin, IsInvestorOrAdmin


class FarmViewSet(viewsets.ModelViewSet):
    serializer_class = FarmSerializer
    filter_backends  = [DjangoFilterBackend]
    filterset_fields = ['flock_type', 'region', 'district', 'is_active']
    search_fields    = ['name', 'region', 'district', 'community']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'farmer':
            return Farm.objects.filter(owner=user)
        if user.role in ('admin', 'investor'):
            return Farm.objects.all()
        return Farm.objects.none()

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsFarmer()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FarmActivityLogViewSet(viewsets.ModelViewSet):
    serializer_class = FarmActivityLogSerializer
    filter_backends  = [DjangoFilterBackend]
    filterset_fields = ['farm', 'date']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'farmer':
            return FarmActivityLog.objects.filter(farm__owner=user)
        if user.role == 'admin':
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
        if user.role in ('admin', 'investor'):
            return FarmAuditReport.objects.all()
        return FarmAuditReport.objects.none()

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(auditor=self.request.user)
