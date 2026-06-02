from rest_framework import viewsets, generics, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .models import Produce, Order, OrderItem, ProduceReview
from .serializers import ProduceSerializer, OrderSerializer, ProduceReviewSerializer
from accounts.permissions import IsFarmer, IsAdmin, IsConsumer


class ProduceViewSet(viewsets.ModelViewSet):
    serializer_class = ProduceSerializer
    filter_backends  = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['produce_type', 'status', 'is_organic']
    search_fields    = ['name', 'farm__name', 'farm__region', 'farm__district']
    ordering_fields  = ['price', 'avg_rating', 'created_at']

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Produce.objects.filter(status='active')
        if user.role == 'farmer':
            return Produce.objects.filter(seller=user)
        return Produce.objects.filter(status='active')

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsFarmer()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user, farm_id=self.request.data.get('farm'))


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    filter_backends  = [DjangoFilterBackend]
    filterset_fields = ['status']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'consumer':
            return Order.objects.filter(buyer=user)
        if user.role == 'farmer':
            return Order.objects.filter(items__produce__seller=user).distinct()
        if user.role == 'admin':
            return Order.objects.all()
        return Order.objects.none()

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status not in ('pending', 'confirmed'):
            return Response({'detail': 'Cannot cancel at this stage.'}, status=400)
        order.status = 'cancelled'
        order.save()
        return Response(OrderSerializer(order).data)


class ProduceReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ProduceReviewSerializer

    def get_queryset(self):
        return ProduceReview.objects.filter(produce_id=self.kwargs['produce_pk'])

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user,
                        produce_id=self.kwargs['produce_pk'])
