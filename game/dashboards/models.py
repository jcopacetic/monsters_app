import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.db import transaction as db_transaction
from django.utils import timezone
from django.utils.text import slugify

User = get_user_model()


class Dashboard(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(max_length=255, unique=True, editable=False)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="dashboard",
    )

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
            return {"success": False, "message": "Amount must be greater than zero."}

        with db_transaction.atomic():
            self.updated_at = timezone.now()

            if transaction_type == "credit":
                self.wallet.balance += amount
                self.wallet.save()
                noti_title = f"You received {amount}gp!"
                noti_description = "Currency has been added to your wallet."
            elif transaction_type == "debit":
                if self.wallet.balance >= amount:
                    self.wallet.balance -= amount
                    self.wallet.save()
                    noti_title = f"You been charged {amount}gp!"
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

            # Create a new transaction record
            Notification.objects.create(
                dashboard=self.wallet.dashboard,
                title=noti_title,
                description=noti_description,
                type="wallet",
            )
            Transaction.objects.create(
                ledger=self,
                type=transaction_type,
                amount=amount,
            )

        return {"success": True, "message": "Transaction successful."}


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
