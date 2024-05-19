from django import template

register = template.Library()


@register.filter
def user_unread_notifications(user):
    return user.dashboard.notifications.filter(read=False).count()
