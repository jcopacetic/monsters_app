from django.urls import path

from game.messaging.views import input_chat
from game.messaging.views import minimize_chat
from game.messaging.views import open_chat
from game.messaging.views import start_chat
from game.messaging.views import toggle_messages_box

app_name = "messaging"

urlpatterns = [
    path("start-chat/<slug:receiver_username>/", view=start_chat, name="start-chat"),
    path("open-chat/<slug:conversation_slug>/", view=open_chat, name="open-chat"),
    path(
        "minimize-chat/<slug:conversation_slug>/",
        view=minimize_chat,
        name="mini-chat",
    ),
    path("toggle-message-box/", view=toggle_messages_box, name="messages-toggle"),
    path("chat-input/<slug:conversation_slug>/", view=input_chat, name="chat-input"),
]
