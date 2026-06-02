from rest_framework import serializers
from .models import Produce, Order, OrderItem, ProduceReview


class ProduceSerializer(serializers.ModelSerializer):
    farm_name   = serializers.CharField(source='farm.name', read_only=True)
    seller_name = serializers.CharField(source='seller.get_full_name', read_only=True)

    class Meta:
        model = Produce
        fields = '__all__'
        read_only_fields = ['id', 'seller', 'avg_rating', 'total_orders', 'created_at', 'updated_at']


class OrderItemSerializer(serializers.ModelSerializer):
    produce_name = serializers.CharField(source='produce.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'produce', 'produce_name', 'quantity', 'unit_price', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items       = OrderItemSerializer(many=True, read_only=True)
    buyer_name  = serializers.CharField(source='buyer.get_full_name', read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['id', 'reference', 'buyer', 'total_amount', 'created_at', 'updated_at']


class ProduceReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.CharField(source='reviewer.get_full_name', read_only=True)

    class Meta:
        model = ProduceReview
        fields = '__all__'
        read_only_fields = ['id', 'reviewer', 'created_at']

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError('Rating must be between 1 and 5.')
        return value
