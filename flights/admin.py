from django.contrib import admin

# Register your models here.
from .models import Airport, Flight, Passenger

admin.site.register(Airport)

class FlightAdmin(admin.ModelAdmin):
    list_display = ("id", "origin", "destination", "duration")

class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",)

admin.site.register(Flight, FlightAdmin)
admin.site.register(Passenger, PassengerAdmin)