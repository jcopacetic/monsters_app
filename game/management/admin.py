from django.contrib import admin

from game.management.models import SystemAnnouncement

models = [SystemAnnouncement]

admin.site.register(models)
