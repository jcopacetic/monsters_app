import uuid

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.db import models
from django.db import transaction as db_transaction
from django.utils import timezone
from django.utils.text import slugify

from game.management.models import SystemAnnouncement

User = get_user_model()


class Dashboard(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(max_length=255, unique=True, editable=False)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="dashboard",
    )

    messages_open = models.BooleanField(default=False, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s dashboard"

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        self.slug = slugify(str(self.uuid))

        if not self.created_at:
            self.created_at = timezone.now()

        super().save(*args, **kwargs)

    def get_conversations(self):
        return self.conversations.all()

    def get_open_conversations(self):
        return self.conversations.filter(controls__open=True, controls__owner=self)


class Wallet(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(max_length=255, unique=True, editable=False)

    dashboard = models.OneToOneField(
        Dashboard,
        on_delete=models.CASCADE,
        related_name="wallet",
    )
    balance = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.dashboard.user.username}'s wallet"

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        self.slug = slugify(str(self.uuid))

        if not self.created_at:
            self.created_at = timezone.now()

        super().save(*args, **kwargs)


class Ledger(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(max_length=255, unique=True, editable=False)

    wallet = models.OneToOneField(
        Wallet,
        on_delete=models.CASCADE,
        related_name="ledger",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.wallet.dashboard.user.username}'s ledger"

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        self.slug = slugify(str(self.uuid))

        if not self.created_at:
            self.created_at = timezone.now()

        super().save(*args, **kwargs)

    def transaction(self, amount, transaction_type):
        if amount <= 0:
            return {
                "success": False,
                "message": "Amount must be greater than zero.",
            }

        original_balance = self.wallet.balance
        channel_layer = get_channel_layer()

        with db_transaction.atomic():
            self.updated_at = timezone.now()

            if transaction_type == "credit":
                self.wallet.balance += amount
                noti_title = f"You received {amount}gp!"
                noti_description = "Currency has been added to your wallet."
            elif transaction_type == "debit":
                if self.wallet.balance >= amount:
                    self.wallet.balance -= amount
                    noti_title = f"You have been charged {amount}gp!"
                    noti_description = "Currency has been removed from your wallet."
                else:
                    return {
                        "success": False,
                        "message": "Insufficient balance.",
                    }
            else:
                return {
                    "success": False,
                    "message": "Invalid transaction type.",
                }

            # Save the wallet and ledger updates
            self.wallet.save(update_fields=["balance", "updated_at"])
            self.save(update_fields=["updated_at"])

            # Create the transaction and notification records
            Transaction.objects.create(
                ledger=self,
                type=transaction_type,
                amount=amount,
            )
            Notification.objects.create(
                dashboard=self.wallet.dashboard,
                title=noti_title,
                description=noti_description,
                type="wallet",
            )

        # Signal the websocket after the transaction is committed
        async_to_sync(channel_layer.group_send)(
            f"group_{self.wallet.dashboard.slug}",
            {
                "type": "manage.currency",
                "original_balance": original_balance,
                "new_balance": self.wallet.balance,
                "transaction_type": transaction_type,
            },
        )

        return {
            "success": True,
            "message": "Transaction successful.",
        }


class Transaction(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(max_length=255, unique=True, editable=False)

    ledger = models.ForeignKey(Ledger, on_delete=models.CASCADE, related_name="items")
    type = models.CharField(
        max_length=10,
        choices=[
            ("debit", "debit"),
            ("credit", "credit"),
        ],
    )

    amount = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ledger item: {self.slug}"

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        self.slug = slugify(str(self.uuid))

        if not self.created_at:
            self.created_at = timezone.now()

        super().save(*args, **kwargs)


class Notification(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(max_length=255, unique=True, editable=False)

    dashboard = models.ForeignKey(
        Dashboard,
        on_delete=models.CASCADE,
        related_name="notifications",
    )
    title = models.CharField(max_length=180)
    description = models.CharField(max_length=180)
    type = models.CharField(
        max_length=10,
        choices=[
            ("wallet", "wallet"),
            ("account", "account"),
        ],
    )
    read = models.BooleanField(default=False, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"ledger item: {self.slug}"

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        self.slug = slugify(str(self.uuid))

        if not self.created_at:
            self.created_at = timezone.now()

        super().save(*args, **kwargs)


class Announcement(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(max_length=255, unique=True, editable=False)

    base_announcement = models.ForeignKey(
        SystemAnnouncement,
        on_delete=models.CASCADE,
        related_name="sent_announcements",
    )

    dashboard = models.ForeignKey(
        Dashboard,
        on_delete=models.CASCADE,
        related_name="announcements",
    )

    read = models.BooleanField(default=False, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"ledger item: {self.slug}"

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        self.slug = slugify(str(self.uuid))

        if not self.created_at:
            self.created_at = timezone.now()

        super().save(*args, **kwargs)
