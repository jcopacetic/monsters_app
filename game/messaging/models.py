import uuid

from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from game.dashboards.models import Dashboard


class Conversation(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        editable=False,
    )

    name = models.CharField(max_length=80, blank=True)

    members = models.ManyToManyField(
        Dashboard,
        blank=True,
        related_name="conversations",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        if not self.slug:
            self.slug = slugify(str(self.uuid))
        if not self.created_at:
            self.created_at = timezone.now()

        super().save(*args, **kwargs)


class Message(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        editable=False,
    )

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    sender = models.ForeignKey(
        Dashboard,
        on_delete=models.CASCADE,
        related_name="messages",
    )

    message = models.CharField(max_length=1200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.created_at}"

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        if not self.slug:
            self.slug = slugify(str(self.uuid))
        if not self.created_at:
            self.created_at = timezone.now()

        super().save(*args, **kwargs)


class ConversationControls(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        editable=False,
    )

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="controls",
    )
    owner = models.ForeignKey(
        Dashboard,
        on_delete=models.CASCADE,
        related_name="conversation_controls",
    )

    open = models.BooleanField(default=False, null=True, blank=True)
    minimized = models.BooleanField(default=True, null=True, blank=True)
    muted = models.BooleanField(default=False, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"{self.owner.user.username}'s controls for chat {self.conversation.slug}"
        )

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        if not self.slug:
            self.slug = slugify(str(self.uuid))
        if not self.created_at:
            self.created_at = timezone.now()

        super().save(*args, **kwargs)
