from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from game.dashboards.models import Announcement
from game.dashboards.models import Dashboard
from game.dashboards.models import Ledger
from game.dashboards.models import Wallet
from game.management.models import SystemAnnouncement

User = get_user_model()


@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if created:
        dashboard = Dashboard.objects.create(user=instance)
        wallet = Wallet.objects.create(dashboard=dashboard)
        ledger = Ledger.objects.create(wallet=wallet)
        ledger.transaction(300, "credit")
        welcome_msg = SystemAnnouncement.objects.filter(type="welcome").first()
        Announcement.objects.create(dashboard=dashboard, base_announcement=welcome_msg)
