from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = 'notifications'

    def ready(self):
        from notifications.credit_signals import register_all
        register_all()
