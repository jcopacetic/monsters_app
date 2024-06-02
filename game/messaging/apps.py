import contextlib

from django.apps import AppConfig


class MessagingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "game.messaging"

    def ready(self):
        with contextlib.suppress(ImportError):
            import game.messaging.signals  # noqa: F401
