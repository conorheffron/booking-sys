"""
Admin module
"""
from django.contrib import admin
from .models import Reservation

class ReservationAdmin(admin.ModelAdmin):
    """ReservationAdmin reservation table config for admin view"""
    list_display = ('id', 'first_name', 'reservation_date', 'reservation_slot')
    list_editable = ('first_name', 'reservation_date', 'reservation_slot')
    search_fields = ('id', 'first_name')
    list_filter = ('reservation_date', 'reservation_slot',)

admin.site.register(Reservation, ReservationAdmin)
