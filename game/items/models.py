import uuid

from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from game.sets.models import Set
from game.utils.model_utils import handle_model_image
from game.utils.options import TYPE_OPTIONS


class Item(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(max_length=255, unique=True, editable=False)

    image = models.ImageField(upload_to="items/", null=True, blank=True)
    tag = models.CharField(max_length=120)
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=220)
    info = models.CharField(max_length=220, blank=True)
    value = models.IntegerField(default=0)
    rarity = models.IntegerField(default=0)
    probability = models.DecimalField(default=1.0, decimal_places=4, max_digits=6)
    set = models.ForeignKey(Set, on_delete=models.CASCADE, related_name="items")
    control_number = models.PositiveIntegerField(default=0)
    sellable = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        self.slug = slugify(str(self.uuid))
        if not self.created_at:
            self.created_at = timezone.now()

        super().save(*args, **kwargs)

        handle_model_image(self.image)


class ConsumableBaseItem(Item):
    health = models.PositiveIntegerField(default=0)
    experience = models.PositiveIntegerField(default=0)


class SlugConsumableBaseItem(Item):
    health = models.PositiveIntegerField(default=0)
    experience = models.PositiveIntegerField(default=0)
    revive = models.BooleanField(default=False, null=True, blank=True)


class ChestBaseItem(Item):
    probability_weight = models.DecimalField(
        default=1.0,
        decimal_places=4,
        max_digits=6,
    )
    min_items = models.PositiveIntegerField(default=2)
    max_items = models.PositiveIntegerField(default=5)
    monster_guarantee = models.PositiveIntegerField(default=0)
    exclude_consumables = models.BooleanField(default=False)
    exclude_currency = models.BooleanField(default=False)
    exclude_moves = models.BooleanField(default=False)
    exclude_monsters = models.BooleanField(default=False)
    exclude_wearables = models.BooleanField(default=False)
    exclude_collectables = models.BooleanField(default=False)
    exclude_chests = models.BooleanField(default=False)
    exclude_slugup = models.BooleanField(default=False)
    exclude_slugconsumable = models.BooleanField(default=False)


class WearableBaseItem(Item):
    WEARABLE_TYPES = [
        ("show", "show"),
        ("offense", "offense"),
        ("defense", "defense"),
    ]
    type = models.CharField(max_length=20, choices=TYPE_OPTIONS)
    wearable_type = models.CharField(
        max_length=20,
        choices=WEARABLE_TYPES,
        default="show",
    )
    health = models.PositiveIntegerField(default=0)
    attack = models.PositiveIntegerField(default=0)
    sp_attack = models.PositiveIntegerField(default=0)
    defense = models.PositiveIntegerField(default=0)
    sp_defense = models.PositiveIntegerField(default=0)
    speed = models.PositiveIntegerField(default=0)
    evasion = models.PositiveIntegerField(default=0)
    accuracy = models.PositiveIntegerField(default=0)


class CurrencyBaseItem(Item):
    min = models.PositiveIntegerField(default=10)
    max = models.PositiveIntegerField(default=50)


class SlugBaseItem(Item):
    pass


class CollectableBaseItem(Item):
    pass


class SlugUpBaseItem(Item):
    attack = models.IntegerField(default=0)
    sp_attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    sp_defense = models.IntegerField(default=0)
    speed = models.IntegerField(default=0)
    evasion = models.IntegerField(default=0)
    accuracy = models.IntegerField(default=0)


class MoveBaseItem(Item):
    damage = models.PositiveIntegerField(default=0)
    total_pp = models.PositiveIntegerField(default=0)
    type_1 = models.CharField(max_length=20, choices=TYPE_OPTIONS)
    type_2 = models.CharField(max_length=20, choices=TYPE_OPTIONS)
    effect_1_chance = models.DecimalField(default=1.0, decimal_places=4, max_digits=6)
    effect_2_chance = models.DecimalField(default=1.0, decimal_places=4, max_digits=6)
