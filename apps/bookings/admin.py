from django.contrib import admin

from apps.bookings.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'rent_property',
        'tenant',
        'start_date',
        'end_date',
        'status',
        'created_at'
    )
    list_filter = (
        'status',
        'created_at',
        'start_date',
        'end_date'
    )
    search_fields = (
        'rent_property__title',
        'tenant__email',
        'tenant__first_name',
        'tenant__last_name',
    )
    ordering = (
        '-created_at',
    )
    autocomplete_fields = (
        'rent_property',
        'tenant'
    )
