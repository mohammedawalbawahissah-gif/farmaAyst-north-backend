import uuid
from django.db import models
from accounts.models import User


class TrainingModule(models.Model):
    class ModuleType(models.TextChoices):
        VIDEO    = 'video',    'Video'
        PDF      = 'pdf',      'PDF Guide'
        AUDIO    = 'audio',    'Audio'
        DOCUMENT = 'document', 'Document'
        WEBINAR  = 'webinar',  'Live Webinar'
        WORKSHOP = 'workshop', 'Workshop'
        QUIZ     = 'quiz',     'Quiz'

    class Level(models.TextChoices):
        BEGINNER     = 'beginner',     'Beginner'
        INTERMEDIATE = 'intermediate', 'Intermediate'
        ADVANCED     = 'advanced',     'Advanced'

    id           = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title        = models.CharField(max_length=300)
    description  = models.TextField()
    module_type  = models.CharField(max_length=20, choices=ModuleType.choices)
    level        = models.CharField(max_length=20, choices=Level.choices, default=Level.BEGINNER)
    topic_tags   = models.JSONField(default=list)  # ['biosecurity','nutrition','records']
    file         = models.FileField(upload_to='training/files/', null=True, blank=True)
    video_url    = models.URLField(blank=True)
    # Webinar / workshop scheduling
    scheduled_at     = models.DateTimeField(null=True, blank=True, help_text='Date & time for live webinar/workshop')
    meeting_url      = models.URLField(blank=True, help_text='Google Meet or Zoom link')
    meeting_platform = models.CharField(max_length=20, blank=True,
                           choices=[('google_meet','Google Meet'),('zoom','Zoom'),('other','Other')])
    duration_minutes = models.PositiveSmallIntegerField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    is_free      = models.BooleanField(default=True)
    created_by   = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'training_modules'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class TrainingEnrolment(models.Model):
    class EnrolmentStatus(models.TextChoices):
        ENROLLED   = 'enrolled',   'Enrolled'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED  = 'completed',  'Completed'

    id        = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    farmer    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrolments')
    module    = models.ForeignKey(TrainingModule, on_delete=models.CASCADE, related_name='enrolments')
    status    = models.CharField(max_length=20, choices=EnrolmentStatus.choices, default=EnrolmentStatus.ENROLLED)
    progress_pct = models.PositiveSmallIntegerField(default=0)
    enrolled_at  = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'training_enrolments'
        unique_together = [('farmer', 'module')]
