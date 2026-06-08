import uuid
from django.db import models
from accounts.models import User


class Notification(models.Model):
    class NotifType(models.TextChoices):
        APPLICATION_STATUS = 'application_status', 'Application Status'
        REPAYMENT_DUE      = 'repayment_due',      'Repayment Due'
        REPAYMENT_RECEIVED = 'repayment_received',  'Repayment Received'
        CONTRACT_SIGNED    = 'contract_signed',     'Contract Signed'
        DISBURSEMENT       = 'disbursement',        'Disbursement'
        ORDER_UPDATE       = 'order_update',        'Order Update'
        TRAINING_NEW       = 'training_new',        'New Training'
        CREDIT_WORKFLOW    = 'credit_workflow',     'Credit Workflow'
        NEW_OPPORTUNITY    = 'new_opportunity',     'New Opportunity'
        AGREEMENT_CREATED  = 'agreement_created',   'Agreement Created'
        CONTRACT_GENERATED = 'contract_generated',  'Contract Generated'
        DISBURSEMENT_REQUESTED = 'disbursement_requested', 'Disbursement Requested'
        DISBURSEMENT_APPROVED  = 'disbursement_approved',  'Disbursement Approved'
        DISBURSEMENT_REJECTED  = 'disbursement_rejected',  'Disbursement Rejected'
        ACTION_REQUIRED    = 'action_required',     'Action Required'
        SYSTEM             = 'system',              'System'

    class Priority(models.TextChoices):
        LOW    = 'low',    'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH   = 'high',   'High'
        URGENT = 'urgent', 'Urgent'

    id                  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notif_type          = models.CharField(max_length=30, choices=NotifType.choices)
    title               = models.CharField(max_length=300)
    body                = models.TextField()
    is_read             = models.BooleanField(default=False)
    priority            = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    data                = models.JSONField(default=dict)
    related_object_type = models.CharField(max_length=50, blank=True)
    related_object_id   = models.CharField(max_length=50, blank=True)
    created_at          = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.notif_type} → {self.recipient.email}'
