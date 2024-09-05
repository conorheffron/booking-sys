"""
Reservation Form Module
"""
from datetime import datetime
from django import forms

class ReservationForm(forms.Form):
    """A Form to make a reservation/booking.
    Attributes:
        first_name  The first name against the reservation.
        reservation_date  The booking date.
        reservation_slot The booking time slot (HH:MM:SS).
    """
    first_name = forms.CharField(min_length=3, max_length = 15)
    reservation_date = forms.DateField(widget=forms.widgets.DateInput(
        attrs={'type': 'date', 'format':['%d-%m-%Y'], 'value': datetime.now().date()}))
    reservation_slot = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type': 'time'}))
