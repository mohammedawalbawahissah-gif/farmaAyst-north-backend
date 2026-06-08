import uuid
from django.db import models
from accounts.models import User


class InputDealerProfile(models.Model):
    class ApprovalStatus(models.TextChoices):
        PENDING   = 'pending',   'Pending'
        APPROVED  = 'approved',  'Approved'
        SUSPENDED = 'suspended', 'Suspended'

    user                = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dealer_profile')
    business_name       = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=100, blank=True)
    region              = models.CharField(max_length=100, blank=True)
    district            = models.CharField(max_length=100, blank=True)
    address             = models.TextField(blank=True)
    phone               = models.CharField(max_length=20, blank=True)
    product_categories  = models.JSONField(default=list)
    approval_status     = models.CharField(max_length=10, choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING)
    approved_by         = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='approved_dealers')
    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'input_dealer_profiles'

    def __str__(self):
        return f'{self.business_name} ({self.user.get_full_name()})'


class FarmInput(models.Model):
    class InputType(models.TextChoices):
        FEED         = 'feed',         'Feed'
        VACCINE      = 'vaccine',      'Vaccine'
        MEDICATION   = 'medication',   'Medication'
        EQUIPMENT    = 'equipment',    'Equipment'
        SUPPLEMENT   = 'supplement',   'Supplement'
        DISINFECTANT = 'disinfectant', 'Disinfectant'
        OTHER        = 'other',        'Other'

    id                 = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    dealer             = models.ForeignKey(User, on_delete=models.CASCADE, related_name='input_listings')
    name               = models.CharField(max_length=200)
    input_type         = models.CharField(max_length=15, choices=InputType.choices)
    brand              = models.CharField(max_length=100, blank=True)
    description        = models.TextField(blank=True)
    unit               = models.CharField(max_length=30)
    price              = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField(default=0)
    min_order_quantity = models.PositiveIntegerField(default=1)
    region             = models.CharField(max_length=100, blank=True)
    is_available       = models.BooleanField(default=True)
    photo              = models.ImageField(upload_to='inputs/', null=True, blank=True)
    created_at         = models.DateTimeField(auto_now_add=True)
    updated_at         = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'farm_inputs'
        ordering = ['-created_at']

    @property
    def dealer_name(self):
        return self.dealer.get_full_name()

    @property
    def business_name(self):
        try:
            return self.dealer.dealer_profile.business_name
        except Exception:
            return ''

    def __str__(self):
        return f'{self.name} ({self.dealer.get_full_name()})'
