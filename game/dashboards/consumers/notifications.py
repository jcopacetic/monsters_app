import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

User = get_user_model()


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["dashboard_slug"]
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
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "notification.send",
                "message": message,
            },
        )

    async def notification_send(self, event):
        template = await self.render_template(
            {"user": self.scope["user"]},
        )
        await self.send(template)

    @sync_to_async
    def render_template(self, context):
        return render_to_string("snippets/alerts-dropdown.html", context)
