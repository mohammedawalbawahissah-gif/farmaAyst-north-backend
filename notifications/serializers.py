from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    # Frontend expects `notification_type` and `message` — alias the backend fields
    notification_type = serializers.CharField(source='notif_type', read_only=True)
    message           = serializers.CharField(source='body', read_only=True)

    class Meta:
        model  = Notification
        fields = [
            'id', 'recipient', 'notification_type', 'notif_type',
            'title', 'message', 'body',
            'is_read', 'priority', 'data',
            'related_object_type', 'related_object_id',
            'created_at',
        ]
        read_only_fields = ['id', 'recipient', 'created_at']
