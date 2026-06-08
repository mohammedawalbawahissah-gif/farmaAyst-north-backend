from rest_framework.routers import DefaultRouter
from .views import InputDealerProfileViewSet, FarmInputViewSet

router = DefaultRouter()
router.register('dealers',  InputDealerProfileViewSet, basename='input-dealer')
router.register('listings', FarmInputViewSet,           basename='farm-input')
urlpatterns = router.urls
