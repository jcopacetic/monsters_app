import logging

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from django.http.response import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.template import Template
from django.template.loader import render_to_string

from game.dashboards.models import Dashboard
from game.messaging.models import Conversation
from game.messaging.models import ConversationControls
from game.messaging.models import Message

User = get_user_model()

logger = logging.getLogger(__name__)


def chat_generator(request, dashboard):
    # Render the conversation panel and chat list templates
    conversations_panel = render_to_string(
        "snippets/chat/conversations-panel.html",
        {"open_conversations": dashboard.get_open_conversations()},
        request,
    )
    chats_list = render_to_string(
        "snippets/chat/chats-list.html",
        {"conversations": dashboard.get_conversations()},
        request,
    )

    # Combine the HTML and render
    bulk_html = chats_list + conversations_panel
    debug_message = f"Bulk HTML generated: {bulk_html}"
    logger.debug(debug_message)

    template = Template(bulk_html)
    context = RequestContext(request)
    return HttpResponse(template.render(context))


def toggle_messages_box(request):
    if request.method == "POST":
        dashboard = Dashboard.objects.get(user=request.user)
        if dashboard.messages_open:
            show_messages = False
            dashboard.messages_open = False
        else:
            show_messages = True
            dashboard.messages_open = True
        dashboard.save()

        context = {
            "show_messages": show_messages,
            "conversations": dashboard.conversations,
            "open_conversations": dashboard.get_open_conversations(),
        }

        return render(request, "snippets/chatbar.html", context)
    return HttpResponse()


def start_chat(request, receiver_username):
    if request.method == "POST":
        receiver = User.objects.get(username=receiver_username)
        debug_message = f"Receiver fetched: {receiver}"
        logger.debug(debug_message)

        # Create a new conversation
        conversation = Conversation.objects.create(
            name=f"{receiver.username}, {request.user.username}",
        )
        debug_message = f"Conversation created: {conversation}"
        logger.debug(debug_message)

        # Add members to the conversation
        conversation.members.add(receiver.dashboard)
        ConversationControls.objects.create(
            conversation=conversation,
            owner=receiver.dashboard,
        )
        conversation.members.add(request.user.dashboard)
        ConversationControls.objects.create(
            open=True,
            conversation=conversation,
            owner=request.user.dashboard,
        )
        debug_message = f"Members added to conversation: {conversation.members.all()}"
        logger.debug(debug_message)

        return chat_generator(request, request.user.dashboard)
    return HttpResponse()


def open_chat(request, conversation_slug):
    if request.method in ["POST", "DELETE"]:
        conversation = Conversation.objects.get(slug=conversation_slug)
        controls = ConversationControls.objects.get(
            conversation=conversation,
            owner=request.user.dashboard,
        )
        if controls.open:
            controls.open = False
        else:
            controls.open = True
            controls.minimized = False
        controls.save()

        return chat_generator(request, request.user.dashboard)
    return HttpResponse()


def minimize_chat(request, conversation_slug):
    if request.method == "POST":
        conversation = Conversation.objects.get(slug=conversation_slug)
        controls = ConversationControls.objects.get(
            conversation=conversation,
            owner=request.user.dashboard,
        )
        if controls.minimized:
            controls.minimized = False
        else:
            controls.minimized = True
        controls.save()
        return chat_generator(request, request.user.dashboard)
    return HttpResponse()


def input_chat(request, conversation_slug):
    if request.method == "POST":
        conversation = Conversation.objects.get(slug=conversation_slug)
        chat_input = request.POST.get("chat-input")
        message = Message.objects.create(
            conversation=conversation,
            sender=request.user.dashboard,
            message=chat_input,
        )

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"group_{conversation.slug}",
            {
                "type": "message.dispatch",
                "message_slug": message.slug,
                "conversation_slug": conversation_slug,
            },
        )

    return HttpResponse()
