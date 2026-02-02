from django.contrib import admin
from .models import Provider, TimeSlot, Booking

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization')
    search_fields = ('user__username',)

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('provider', 'start_time', 'end_time', 'is_booked')
    list_filter = ('is_booked', 'provider')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client', 'slot', 'created_at')
