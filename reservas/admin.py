from django.contrib import admin
from .models import Resource, Booking

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'resource_type', 'description')
    list_filter = ('resource_type',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'resource', 'start_time', 'end_time', 'is_recurring')
    list_filter = ('resource', 'start_time')