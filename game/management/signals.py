from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from game.dashboards.models import Announcement
from game.management.models import SystemAnnouncement

User = get_user_model()


@receiver(post_save, sender=SystemAnnouncement)
def create_system_announcement(sender, instance, created, **kwargs):
    if created:
        if instance.type == "system":
            for user in User.objects.all():
                Announcement.objects.create(
                    dashboard=user.dashboard,
                    base_announcement=instance,
                )
