from django.shortcuts import render

from game.items.models import Item


def itemslist(request):
    items = Item.objects.all()
    return render(
        request,
        "items/items_list.html",
        {"items": items},
    )
