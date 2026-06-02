from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, FarmerProfile, InvestorProfile
from .serializers import (UserSerializer, RegisterSerializer,
                          FarmerProfileSerializer, InvestorProfileSerializer,
                          ChangePasswordSerializer)
from .permissions import IsAdmin, IsFarmer, IsInvestor


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        }, status=status.HTTP_201_CREATED)


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh = RefreshToken(request.data['refresh'])
            refresh.blacklist()
            return Response({'detail': 'Logged out successfully.'})
        except Exception:
            return Response({'detail': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({'detail': 'Password updated successfully.'})


class FarmerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = FarmerProfileSerializer
    permission_classes = [IsFarmer]

    def get_object(self):
        profile, _ = FarmerProfile.objects.get_or_create(user=self.request.user)
        return profile


class InvestorProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = InvestorProfileSerializer
    permission_classes = [IsInvestor]

    def get_object(self):
        profile, _ = InvestorProfile.objects.get_or_create(user=self.request.user)
        return profile


class UserViewSet(viewsets.ModelViewSet):
    """Admin-only user management."""
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['role', 'is_verified', 'is_active']
    search_fields = ['email', 'first_name', 'last_name', 'phone']

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        user = self.get_object()
        user.is_verified = True
        user.save()
        if hasattr(user, 'farmer_profile'):
            user.farmer_profile.verification_status = 'verified'
            user.farmer_profile.save()
        return Response({'detail': f'{user.get_full_name()} verified.'})

    @action(detail=True, methods=['post'])
    def suspend(self, request, pk=None):
        user = self.get_object()
        user.is_active = False
        user.save()
        return Response({'detail': f'{user.get_full_name()} suspended.'})
