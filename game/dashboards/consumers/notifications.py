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
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "notification.send",
            },
        )

    async def notification_send(self, event):
        template = await self.render_template(
            {"user": self.scope["user"]},
            "snippets/alerts-dropdown.html",
        )
        await self.send(template)

    async def announcement_send(self, event):
        template = await self.render_template(
            {"user": self.scope["user"]},
            "snippets/announcement-dropdown.html",
        )
        await self.send(template)

    async def manage_currency(self, event):
        transaction_type = event["transaction_type"]
        template = await self.render_template(
            {
                "user": self.scope["user"],
                "transaction_type": transaction_type,
                "original_balance": event["original_balance"],
                "new_balance": event["new_balance"],
            },
            "snippets/header-currency.html",
        )
        await self.send(template)

    @sync_to_async
    def render_template(self, context, template_path):
        return render_to_string(template_path, context)
