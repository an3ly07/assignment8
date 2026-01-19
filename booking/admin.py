from django.contrib import admin
from .models import Provider, TimeSlot, Booking

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization')
    search_fields = ('user__username',)


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('provider', 'start_time', 'end_time', 'is_available')
    list_filter = ('provider', 'is_available')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client', 'time_slot', 'created_at', 'is_cancelled')
    list_filter = ('is_cancelled',)
    search_fields = ('client__username',)
