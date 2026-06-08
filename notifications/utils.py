from .models import Notification


def send_notification(user, notif_type, title, body, data=None, priority='medium', related_obj=None):
    """
    Create an in-app notification record.
    Safe to call even before optional fields exist — Django will use column defaults.
    """
    try:
        Notification.objects.create(
            recipient=user,
            notif_type=notif_type,
            title=title,
            body=body,
            priority=priority,
            data=data or {},
            related_object_type=related_obj.__class__.__name__ if related_obj else '',
            related_object_id=str(related_obj.pk) if related_obj else '',
        )
    except Exception as exc:
        # Log but never let a notification failure crash a business transaction
        import logging
        logging.getLogger(__name__).warning('send_notification failed: %s', exc)


def create_notification(user, title, message, notification_type='system', priority='medium', related_obj=None):
    """Alias kept for backward-compatibility with farms/views.py and other callers."""
    send_notification(user, notification_type, title, message, priority=priority, related_obj=related_obj)


def notify_admins(notif_type, title, body, priority='medium', related_obj=None):
    """Broadcast a notification to every active admin."""
    from accounts.models import User
    for admin in User.objects.filter(role='admin', is_active=True):
        send_notification(admin, notif_type, title, body, priority=priority, related_obj=related_obj)
