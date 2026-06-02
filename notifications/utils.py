from .models import Notification


def send_notification(user, notif_type, title, body, data=None):
    """Create an in-app notification. Extend to push/SMS here."""
    Notification.objects.create(
        recipient=user,
        notif_type=notif_type,
        title=title,
        body=body,
        data=data or {},
    )
    # TODO: trigger Firebase push notification
    # TODO: trigger Hubtel SMS for critical alerts
