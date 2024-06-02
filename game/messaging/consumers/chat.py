from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string

from game.dashboards.models import Dashboard
from game.messaging.models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["conversation_slug"]
        self.room_group_name = f"group_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        pass

    async def message_dispatch(self, event):
        message_slug = event["message_slug"]
        conversation_slug = event["conversation_slug"]
        message = await self.get_message(message_slug)
        sender = await self.get_sender(message)
        user_dashboard = await self.get_receiver()
        message_context = "sender" if sender == user_dashboard else "receiver"
        template = await self.render_template(
            conversation_slug,
            {"message": message, "message_context": message_context},
            "snippets/chat/message.html",
        )
        await self.send(template)

    async def render_template(self, conversation_slug, context, template_path):
        return (
            f'<div id="messages-{conversation_slug}" hx-swap-oob="beforeend">'
            + render_to_string(template_path, context)
            + "</div>"
        )

    @database_sync_to_async
    def get_message(self, message_slug):
        return Message.objects.get(slug=message_slug)

    @database_sync_to_async
    def get_sender(self, message):
        return message.sender

    @database_sync_to_async
    def get_receiver(self):
        user = self.scope["user"]
        return Dashboard.objects.get(user=user)
