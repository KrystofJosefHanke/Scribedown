from django.contrib import admin
from .models import World, Character, Location, Event, Item, Race, WikiCategory, WikiPage, WikiLink

admin.site.register(World)
admin.site.register(Character)
admin.site.register(Location)
admin.site.register(Event)
admin.site.register(Item)
admin.site.register(Race)
admin.site.register(WikiCategory)
admin.site.register(WikiPage)
admin.site.register(WikiLink)
