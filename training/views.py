from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import TrainingModule, TrainingEnrolment
from .serializers import TrainingModuleSerializer, TrainingEnrolmentSerializer
from accounts.permissions import IsAdmin, IsFarmer


class TrainingModuleViewSet(viewsets.ModelViewSet):
    queryset = TrainingModule.objects.filter(is_published=True)
    serializer_class = TrainingModuleSerializer
    filter_backends  = [DjangoFilterBackend]
    filterset_fields = ['module_type', 'level', 'is_free']
    search_fields    = ['title', 'description']

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.role == 'admin':
            return TrainingModule.objects.all()
        return TrainingModule.objects.filter(is_published=True)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TrainingEnrolmentViewSet(viewsets.ModelViewSet):
    serializer_class = TrainingEnrolmentSerializer
    permission_classes = [IsFarmer]

    def get_queryset(self):
        return TrainingEnrolment.objects.filter(farmer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)

    @action(detail=True, methods=['post'])
    def update_progress(self, request, pk=None):
        enrolment = self.get_object()
        pct = int(request.data.get('progress_pct', 0))
        enrolment.progress_pct = min(100, pct)
        if enrolment.progress_pct == 100:
            enrolment.status = 'completed'
            enrolment.completed_at = timezone.now()
        elif enrolment.progress_pct > 0:
            enrolment.status = 'in_progress'
        enrolment.save()
        return Response(TrainingEnrolmentSerializer(enrolment).data)
