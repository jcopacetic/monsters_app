from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from game.dashboards.models import Notification


@receiver(post_save, sender=Notification)
def create_notification(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"group_{instance.dashboard.slug}",
            {
                "type": "notification.send",
                "message": "1",
            },
        )
