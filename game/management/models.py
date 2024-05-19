import uuid

from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class SystemAnnouncement(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(max_length=255, unique=True, editable=False)

    title = models.CharField(max_length=180)
    description = models.TextField(max_length=3600)
    type = models.CharField(
        max_length=10,
        choices=[
            ("welcome", "welcome"),
            ("account", "account"),
            ("system", "system"),
            ("season", "season"),
            ("story", "story"),
            ("store", "store"),
        ],
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        self.slug = slugify(str(self.uuid))

        if not self.created_at:
            self.created_at = timezone.now()

        super().save(*args, **kwargs)
