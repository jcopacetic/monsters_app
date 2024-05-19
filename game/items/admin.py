from django.contrib import admin

from game.items.models import ChestBaseItem
from game.items.models import CollectableBaseItem
from game.items.models import ConsumableBaseItem
from game.items.models import CurrencyBaseItem
from game.items.models import MoveBaseItem
from game.items.models import SlugBaseItem
from game.items.models import SlugConsumableBaseItem
from game.items.models import SlugUpBaseItem
from game.items.models import WearableBaseItem

models = [
    ConsumableBaseItem,
    SlugConsumableBaseItem,
    ChestBaseItem,
    WearableBaseItem,
    CurrencyBaseItem,
    SlugBaseItem,
    CollectableBaseItem,
    SlugUpBaseItem,
    MoveBaseItem,
]

admin.site.register(models)
