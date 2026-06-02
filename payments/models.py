import uuid
from django.db import models
from accounts.models import User
from credit.models import CreditAgreement


class Disbursement(models.Model):
    class Method(models.TextChoices):
        MOMO     = 'momo',     'MTN MoMo'
        PAYSTACK = 'paystack', 'Paystack'
        CASH     = 'cash',     'Cash'
        IN_KIND  = 'in_kind',  'In-Kind (Inputs)'

    class Status(models.TextChoices):
        PENDING   = 'pending',   'Pending'
        PROCESSING = 'processing', 'Processing'
        COMPLETED = 'completed', 'Completed'
        FAILED    = 'failed',    'Failed'

    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference    = models.CharField(max_length=30, unique=True, blank=True)
    agreement    = models.ForeignKey(CreditAgreement, on_delete=models.CASCADE, related_name='disbursements')
    amount       = models.DecimalField(max_digits=12, decimal_places=2)
    method       = models.CharField(max_length=20, choices=Method.choices)
    status       = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    gateway_ref  = models.CharField(max_length=200, blank=True)
    gateway_response = models.JSONField(default=dict)
    disbursed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    notes        = models.TextField(blank=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'disbursements'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.reference:
            count = Disbursement.objects.count() + 1
            self.reference = f'DIS-{count:05d}'
        super().save(*args, **kwargs)


class RepaymentSchedule(models.Model):
    class ScheduleStatus(models.TextChoices):
        UPCOMING  = 'upcoming',  'Upcoming'
        DUE       = 'due',       'Due'
        PAID      = 'paid',      'Paid'
        OVERDUE   = 'overdue',   'Overdue'
        WAIVED    = 'waived',    'Waived'

    id          = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agreement   = models.ForeignKey(CreditAgreement, on_delete=models.CASCADE, related_name='repayment_schedule')
    installment_number = models.PositiveSmallIntegerField()
    due_date    = models.DateField()
    amount_due  = models.DecimalField(max_digits=12, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status      = models.CharField(max_length=20, choices=ScheduleStatus.choices, default=ScheduleStatus.UPCOMING)
    paid_at     = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'repayment_schedules'
        ordering = ['due_date']


class Payment(models.Model):
    class PaymentType(models.TextChoices):
        REPAYMENT    = 'repayment',    'Repayment'
        MARKETPLACE  = 'marketplace',  'Marketplace Order'

    class PaymentStatus(models.TextChoices):
        PENDING   = 'pending',   'Pending'
        SUCCESS   = 'success',   'Successful'
        FAILED    = 'failed',    'Failed'
        REFUNDED  = 'refunded',  'Refunded'

    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference    = models.CharField(max_length=30, unique=True, blank=True)
    payer        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments_made')
    payment_type = models.CharField(max_length=20, choices=PaymentType.choices)
    amount       = models.DecimalField(max_digits=12, decimal_places=2)
    currency     = models.CharField(max_length=5, default='GHS')
    method       = models.CharField(max_length=20, choices=Disbursement.Method.choices)
    status       = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    schedule     = models.ForeignKey(RepaymentSchedule, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    gateway_ref  = models.CharField(max_length=200, blank=True)
    gateway_response = models.JSONField(default=dict)
    phone_number = models.CharField(max_length=20, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.reference:
            count = Payment.objects.count() + 1
            self.reference = f'PAY-{count:06d}'
        super().save(*args, **kwargs)
