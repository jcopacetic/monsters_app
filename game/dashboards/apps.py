import contextlib

from django.apps import AppConfig


class DashboardsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "game.dashboards"

    def ready(self):
        with contextlib.suppress(ImportError):
            import game.dashboards.signals  # noqa: F401
