from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class   = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notif = self.get_object()
        notif.is_read = True
        notif.save()
        return Response({'detail': 'Marked as read.'})

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        self.get_queryset().update(is_read=True)
        return Response({'detail': 'All notifications marked as read.'})

    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'unread': count})

    @action(detail=False, methods=['get'])
    def credit_workflow(self, request):
        """Return only credit-workflow notifications for the requesting user."""
        qs = self.get_queryset().filter(notif_type='credit_workflow')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def resend(self, request, pk=None):
        """Admin: re-create a notification so the recipient sees it again."""
        notif = self.get_object()
        Notification.objects.create(
            recipient=notif.recipient,
            notif_type=notif.notif_type,
            title=f'[Resent] {notif.title}',
            body=notif.body,
            priority=notif.priority,
            data=notif.data,
        )
        return Response({'detail': 'Notification resent.'})
