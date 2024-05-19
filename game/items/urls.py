from django.urls import path

from game.items.views import itemslist

app_name = "items"

urlpatterns = [
    path("", itemslist, name="list"),
]
