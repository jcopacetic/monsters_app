from django import template

from game.messaging.models import ConversationControls

register = template.Library()


@register.simple_tag
def chat_minimized_check(conversation, dashboard):
    controls = ConversationControls.objects.get(
        conversation=conversation,
        owner=dashboard,
    )
    return controls.minimized


@register.simple_tag
def chat_name(conversation, user):
    members = conversation.members.exclude(pk=user.pk)
    return ", ".join(member.user.username for member in members)


@register.simple_tag
def chat_time(message):
    return message.created_at if message else "now"
