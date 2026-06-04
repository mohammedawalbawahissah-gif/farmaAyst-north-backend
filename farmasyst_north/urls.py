from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import (RegisterView, LogoutView, MeView, ChangePasswordView,
                             FarmerProfileView, InvestorProfileView,
                             FarmerProfileListView, FarmerProfileDetailView,
                             InvestorProfileListView,
                             UserViewSet, VerifiedTokenObtainPairView)
from farms.views import FarmViewSet, FarmActivityLogViewSet, FarmAuditReportViewSet
from credit.views import CreditApplicationViewSet, DocumentUploadView, CreditAgreementViewSet
from marketplace.views import ProduceViewSet, OrderViewSet, ProduceReviewViewSet
from training.views import TrainingModuleViewSet, TrainingEnrolmentViewSet
from notifications.views import NotificationViewSet
from payments.views import (RepaymentScheduleViewSet, InitiateRepaymentView,
                             PaystackWebhookView, DisbursementViewSet,
                             DisbursementRequestViewSet, PayFullBalanceView)

router = DefaultRouter()
router.register(r'users',               UserViewSet,              basename='users')
router.register(r'farms',               FarmViewSet,              basename='farms')
router.register(r'farms/(?P<farm_pk>[^/.]+)/activity-logs', FarmActivityLogViewSet, basename='farm-activity')
router.register(r'farm-audit-reports',  FarmAuditReportViewSet,   basename='audit-reports')
router.register(r'credit/applications', CreditApplicationViewSet, basename='credit-applications')
router.register(r'credit/agreements',   CreditAgreementViewSet,   basename='credit-agreements')
router.register(r'marketplace/produce', ProduceViewSet,           basename='produce')
router.register(r'marketplace/produce/(?P<produce_pk>[^/.]+)/reviews', ProduceReviewViewSet, basename='produce-reviews')
router.register(r'marketplace/orders',  OrderViewSet,             basename='orders')
router.register(r'training/modules',    TrainingModuleViewSet,    basename='training-modules')
router.register(r'training/enrolments', TrainingEnrolmentViewSet, basename='enrolments')
router.register(r'notifications',       NotificationViewSet,      basename='notifications')
router.register(r'payments/schedules',  RepaymentScheduleViewSet, basename='repayment-schedules')
router.register(r'payments/disbursements', DisbursementViewSet,   basename='disbursements')
router.register(r'payments/disbursement-requests', DisbursementRequestViewSet, basename='disbursement-requests')

urlpatterns = [
    path('admin/',                         admin.site.urls),
    path('api/v1/',                        include(router.urls)),

    # Auth
    path('api/v1/auth/register/',          RegisterView.as_view()),
    path('api/v1/auth/login/',             VerifiedTokenObtainPairView.as_view()),
    path('api/v1/auth/refresh/',           TokenRefreshView.as_view()),
    path('api/v1/auth/logout/',            LogoutView.as_view()),
    path('api/v1/auth/me/',                MeView.as_view()),
    path('api/v1/auth/change-password/',   ChangePasswordView.as_view()),

    # Profiles
    path('api/v1/profiles/farmer/',         FarmerProfileView.as_view()),
    path('api/v1/profiles/farmers/',          FarmerProfileListView.as_view()),
    path('api/v1/profiles/farmers/<int:pk>/', FarmerProfileDetailView.as_view()),
    path('api/v1/profiles/investor/',       InvestorProfileView.as_view()),
    path('api/v1/profiles/investors/',      InvestorProfileListView.as_view()),

    # Credit documents
    path('api/v1/credit/applications/<uuid:application_id>/documents/',
         DocumentUploadView.as_view()),

    # Payments
    path('api/v1/payments/initiate-repayment/', InitiateRepaymentView.as_view()),
    path('api/v1/payments/pay-full-balance/',   PayFullBalanceView.as_view()),
    path('api/v1/webhooks/paystack/',           PaystackWebhookView.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
