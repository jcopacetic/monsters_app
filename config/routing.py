from django.urls import path

from game.dashboards.consumers.notifications import NotificationConsumer

websocket_urlpatterns = [
    path("ws/messages/<slug:dashboard_slug>/", NotificationConsumer.as_asgi()),
]
