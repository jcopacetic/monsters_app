from django.shortcuts import render


def dashboard(request):
    dashboard = request.user.dashboard

    context = {
        "page_title": "Dashboard",
        "dashboard": dashboard,
    }
    return render(request, "dashboard/dashboard.html", context)


def wallet(request):
    wallet = request.user.dashboard.wallet

    context = {
        "page_title": "Wallet",
        "wallet": wallet,
    }
    return render(request, "dashboard/wallet.html", context)


# HTMX ENDPOINTS


## HTMX NOTIFICATION ENDPOINTS
def clear_notification_indicator(request):
    unread_notifications = request.user.dashboard.notifications.filter(read=False)
    for notification in unread_notifications:
        notification.read = True
        notification.save()

    context = {
        "user": request.user,
    }

    return render(request, "snippets/notification-indicator.html", context)
