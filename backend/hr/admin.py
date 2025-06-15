"""
Admin module
"""
from django.contrib import admin
from .models import Reservation

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'reservation_date', 'reservation_slot')  # Fields to display in the list view
    list_editable = ('first_name', 'reservation_date', 'reservation_slot')  # Fields to edit in the list view
    search_fields = ('id', 'first_name')  # Add a search bar for these fields
    list_filter = ('reservation_date', 'reservation_slot',)  # Add filters for these fields

admin.site.register(Reservation, ReservationAdmin)
