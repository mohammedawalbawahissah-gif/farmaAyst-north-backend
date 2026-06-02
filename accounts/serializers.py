from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, FarmerProfile, InvestorProfile


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id','email','first_name','last_name','full_name','phone','role',
                  'is_verified','profile_photo','language','date_joined']
        read_only_fields = ['id','is_verified','date_joined']

    def get_full_name(self, obj):
        return obj.get_full_name()


class RegisterSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email','first_name','last_name','phone','role','password','password2','language']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)


class FarmerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = FarmerProfile
        fields = '__all__'
        read_only_fields = ['user', 'credit_score', 'credit_score_updated_at', 'verification_status']


class InvestorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = InvestorProfile
        fields = '__all__'
        read_only_fields = ['user', 'is_kyc_verified']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect.')
        return value
