from rest_framework.routers import DefaultRouter
from .views import VetProfileViewSet, VetServiceViewSet, VetBookingViewSet

router = DefaultRouter()
router.register('profiles', VetProfileViewSet, basename='vet-profile')
router.register('services', VetServiceViewSet, basename='vet-service')
router.register('bookings', VetBookingViewSet, basename='vet-booking')
urlpatterns = router.urls
