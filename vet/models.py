import uuid
import random
import string
from django.db import models
from accounts.models import User


class VetProfile(models.Model):
    class ApprovalStatus(models.TextChoices):
        PENDING   = 'pending',   'Pending'
        APPROVED  = 'approved',  'Approved'
        SUSPENDED = 'suspended', 'Suspended'

    user             = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vet_profile')
    license_number   = models.CharField(max_length=50, unique=True)
    specialisation   = models.CharField(max_length=200, blank=True)
    clinic_name      = models.CharField(max_length=200)
    region           = models.CharField(max_length=100, blank=True)
    district         = models.CharField(max_length=100, blank=True)
    phone            = models.CharField(max_length=20, blank=True)
    is_available     = models.BooleanField(default=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    services_offered = models.TextField(blank=True)
    approval_status  = models.CharField(max_length=10, choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING)
    approved_by      = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='approved_vets')
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'vet_profiles'

    def __str__(self):
        return f'Dr. {self.user.get_full_name()} — {self.clinic_name}'


class VetService(models.Model):
    class ServiceType(models.TextChoices):
        VACCINATION  = 'vaccination',  'Vaccination'
        DIAGNOSIS    = 'diagnosis',    'Diagnosis'
        TREATMENT    = 'treatment',    'Treatment'
        CONSULTATION = 'consultation', 'Consultation'
        FARM_VISIT   = 'farm_visit',   'Farm Visit'
        OTHER        = 'other',        'Other'

    id               = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vet              = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vet_services')
    service_name     = models.CharField(max_length=200)
    service_type     = models.CharField(max_length=20, choices=ServiceType.choices)
    description      = models.TextField(blank=True)
    price            = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.PositiveIntegerField(default=30)
    is_mobile        = models.BooleanField(default=False)
    region           = models.CharField(max_length=100, blank=True)
    is_active        = models.BooleanField(default=True)
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vet_services'
        ordering = ['service_name']

    @property
    def vet_name(self):
        return self.vet.get_full_name()

    @property
    def vet_clinic(self):
        try:
            return self.vet.vet_profile.clinic_name
        except Exception:
            return ''

    def __str__(self):
        return f'{self.service_name} ({self.vet.get_full_name()})'


class VetBooking(models.Model):
    class Status(models.TextChoices):
        PENDING   = 'pending',   'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    class VisitType(models.TextChoices):
        ON_FARM      = 'on_farm',      'On Farm'
        CLINIC       = 'clinic',       'Clinic'
        TELEMEDICINE = 'telemedicine', 'Telemedicine'

    id                = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference         = models.CharField(max_length=20, unique=True, blank=True)
    farmer            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vet_bookings')
    vet               = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vet_appointments')
    farm              = models.ForeignKey('farms.Farm', null=True, blank=True, on_delete=models.SET_NULL)
    service           = models.ForeignKey(VetService, null=True, blank=True, on_delete=models.SET_NULL)
    booking_date      = models.DateTimeField()
    visit_type        = models.CharField(max_length=15, choices=VisitType.choices, default=VisitType.ON_FARM)
    issue_description = models.TextField()
    status            = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    fee               = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vet_notes         = models.TextField(blank=True)
    created_at        = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'vet_bookings'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = 'VB-' + ''.join(random.choices(string.digits, k=6))
        if self.service and not self.fee:
            self.fee = self.service.price
        super().save(*args, **kwargs)

    @property
    def farmer_name(self):
        return self.farmer.get_full_name()

    @property
    def vet_name(self):
        return self.vet.get_full_name()

    @property
    def farm_name(self):
        return self.farm.name if self.farm else None

    @property
    def service_name(self):
        return self.service.service_name if self.service else ''

    def __str__(self):
        return f'{self.reference} — {self.farmer_name}'
