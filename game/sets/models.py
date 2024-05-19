import uuid

from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from game.utils.model_utils import handle_model_image


class Set(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(max_length=255, unique=True, editable=False)

    name = models.CharField(max_length=180)
    badge = models.ImageField(upload_to="set-badges/", null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.uuid)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        self.slug = slugify(str(self.uuid))
        if not self.created_at:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

        handle_model_image(self.badge)
