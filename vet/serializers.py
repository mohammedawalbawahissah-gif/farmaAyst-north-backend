from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import VetProfile, VetService, VetBooking


class VetProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = VetProfile
        fields = '__all__'
        read_only_fields = ['id', 'user', 'approval_status', 'approved_by', 'created_at', 'updated_at']


class VetServiceSerializer(serializers.ModelSerializer):
    vet_name   = serializers.ReadOnlyField()
    vet_clinic = serializers.ReadOnlyField()

    class Meta:
        model = VetService
        fields = '__all__'
        read_only_fields = ['id', 'vet', 'created_at']


class VetBookingSerializer(serializers.ModelSerializer):
    farmer_name  = serializers.ReadOnlyField()
    vet_name     = serializers.ReadOnlyField()
    farm_name    = serializers.ReadOnlyField()
    service_name = serializers.ReadOnlyField()

    class Meta:
        model = VetBooking
        fields = '__all__'
        read_only_fields = ['id', 'reference', 'farmer', 'fee', 'vet_notes', 'created_at']
