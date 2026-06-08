from decimal import Decimal
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db import transaction
from .models import Produce, Order, OrderItem, ProduceReview
from .serializers import ProduceSerializer, OrderSerializer, ProduceReviewSerializer
from accounts.permissions import IsFarmer, IsAdmin
from notifications.models import Notification


def _notify(recipient, notif_type, title, body, data=None):
    try:
        Notification.objects.create(
            recipient=recipient, notif_type=notif_type,
            title=title, body=body, data=data or {},
        )
    except Exception:
        pass


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
        serializer.save(
            seller=self.request.user,
            farm_id=self.request.data.get('farm'),
        )


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class   = OrderSerializer
    filter_backends    = [DjangoFilterBackend]
    filterset_fields   = ['status']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'consumer':
            return Order.objects.prefetch_related('items__produce').filter(buyer=user)
        if user.role == 'farmer':
            return Order.objects.prefetch_related('items__produce').filter(
                items__produce__seller=user
            ).distinct()
        if user.role == 'admin':
            return Order.objects.prefetch_related('items__produce').all()
        return Order.objects.none()

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Fully manual create — bypass DRF serializer validation on input
        so that choice-field defaults set in this method don't cause 400s.
        """
        data           = request.data
        produce_id     = data.get('produce_id')
        delivery_type  = data.get('delivery_type', 'pickup')
        delivery_addr  = data.get('delivery_address', '') or ''
        delivery_date  = data.get('delivery_date') or None
        notes          = data.get('notes', '') or ''
        raw_pm = data.get('payment_method', 'momo')
        pm_map = {
            'instant': 'momo', 'momo': 'momo',
            'card': 'card', 'paystack': 'card',
            'bank_transfer': 'bank_transfer',
            'cod': 'cash_on_delivery', 'cash_on_delivery': 'cash_on_delivery',
        }
        payment_method = pm_map.get(raw_pm, 'cash_on_delivery')

        try:
            quantity = Decimal(str(data.get('quantity', 1)))
        except Exception:
            quantity = Decimal('1')

        if not produce_id:
            return Response({'detail': 'produce_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            produce = Produce.objects.select_related('seller', 'farm').get(
                id=produce_id, status='active'
            )
        except Produce.DoesNotExist:
            return Response(
                {'detail': 'Produce not found or no longer available.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if delivery_type == 'delivery' and not delivery_addr.strip():
            return Response(
                {'detail': 'Delivery address is required for home delivery.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        subtotal = produce.price * quantity

        order = Order.objects.create(
            buyer            = request.user,
            delivery_type    = delivery_type,
            delivery_address = delivery_addr,
            delivery_date    = delivery_date,
            notes            = notes,
            total_amount     = subtotal,
            status           = Order.OrderStatus.PENDING,
            payment_method   = payment_method,
        )

        OrderItem.objects.create(
            order      = order,
            produce    = produce,
            quantity   = quantity,
            unit_price = produce.price,
            subtotal   = subtotal,
        )

        produce.quantity_available = max(Decimal('0'), produce.quantity_available - quantity)
        produce.total_orders       = produce.total_orders + 1
        if produce.quantity_available == 0:
            produce.status = 'sold_out'
        produce.save()

        buyer_name     = request.user.get_full_name() or request.user.email
        farm_name      = produce.farm.name if produce.farm else 'your farm'
        delivery_label = 'Farm Pickup' if delivery_type == 'pickup' else 'Home Delivery'
        pay_label      = 'Instant (MoMo/Card)' if payment_method == 'instant' else 'Cash on Delivery'

        _notify(
            recipient  = produce.seller,
            notif_type = 'order_update',
            title      = f'New order — {produce.name}',
            body       = (
                f'{buyer_name} ordered {quantity} {produce.unit} of {produce.name} '
                f'(GHS {float(subtotal):,.2f}). Fulfilment: {delivery_label}. '
                f'Payment: {pay_label}. Ref: {order.reference}.'
            ),
            data={'order_id': str(order.id), 'order_reference': order.reference},
        )
        _notify(
            recipient  = request.user,
            notif_type = 'order_update',
            title      = f'Order placed — {order.reference}',
            body       = (
                f'Your order for {quantity} {produce.unit} of {produce.name} '
                f'from {farm_name} was placed. The farmer will confirm shortly.'
            ),
            data={'order_id': str(order.id), 'order_reference': order.reference},
        )

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        order = self.get_object()
        if order.status != 'pending':
            return Response({'detail': 'Only pending orders can be confirmed.'}, status=400)
        order.status = 'confirmed'
        order.save()
        _notify(
            recipient  = order.buyer,
            notif_type = 'order_update',
            title      = f'Order confirmed — {order.reference}',
            body       = f'The farmer confirmed your order {order.reference}. Preparing for {order.get_delivery_type_display().lower()}.',
            data={'order_id': str(order.id)},
        )
        return Response(OrderSerializer(order).data)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status not in ('pending', 'confirmed'):
            return Response({'detail': 'Cannot cancel at this stage.'}, status=400)
        order.status = 'cancelled'
        order.save()
        if request.user.role == 'farmer':
            _notify(
                recipient  = order.buyer,
                notif_type = 'order_update',
                title      = f'Order cancelled — {order.reference}',
                body       = f'Your order {order.reference} was cancelled by the seller.',
                data={'order_id': str(order.id)},
            )
        return Response(OrderSerializer(order).data)


class ProduceReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ProduceReviewSerializer

    def get_queryset(self):
        return ProduceReview.objects.filter(produce_id=self.kwargs['produce_pk'])

    def perform_create(self, serializer):
        serializer.save(
            reviewer=self.request.user,
            produce_id=self.kwargs['produce_pk'],
        )
