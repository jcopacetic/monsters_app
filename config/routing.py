from django.urls import path

from game.dashboards.consumers.notifications import NotificationConsumer
from game.messaging.consumers.chat import ChatConsumer

websocket_urlpatterns = [
    path("ws/messages/<slug:dashboard_slug>/", NotificationConsumer.as_asgi()),
    path("ws/chat/<slug:conversation_slug>/", ChatConsumer.as_asgi()),
]
