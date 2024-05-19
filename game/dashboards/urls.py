from django.urls import path

from game.dashboards.views import clear_announcement_indicator
from game.dashboards.views import clear_notification_indicator
from game.dashboards.views import dashboard
from game.dashboards.views import wallet

app_name = "dashboards"

urlpatterns = [
    path("", view=dashboard, name="dashboard"),
    path("wallet/", view=wallet, name="wallet"),
    path("read-notifications/", view=clear_notification_indicator, name="read-notifs"),
    path(
        "read-announcements/",
        view=clear_announcement_indicator,
        name="read-announce",
    ),
]
