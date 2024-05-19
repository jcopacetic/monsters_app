from django.contrib import admin

from game.sets.models import Set

models = [Set]

admin.site.register(models)
