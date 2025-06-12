"""
Reservation Form Module
"""
from datetime import time
from django import forms
from .time_utils import TimeUtils

class EditReservationForm(forms.Form):
    """
    A Django form for editing an existing reservation's date and time slot.

    Fields
    ------
    reservation_date : DateField
        The new date for the reservation.
    reservation_slot : TimeField
        The new time slot for the reservation (HH:MM).

    Usage
    -----
    Used in views to process user input when updating an existing reservation.
    Validates that both date and time are provided and in the correct formats.
    """
    reservation_date = forms.DateField(label='', widget=forms.widgets.DateInput(
        attrs={'type': 'date', 'class': 'form-control'}
    ))
    reservation_slot = forms.TimeField(label='', widget=forms.widgets.TimeInput(
        attrs={'type': 'time', 'class': 'form-control'}
    ))

class ReservationForm(forms.Form):
    """A Form to make a reservation/booking.
    Attributes:
        first_name  The first name against the reservation.
        reservation_date  The booking date.
        reservation_slot The booking time slot (HH:MM).
    """
    time_utils = TimeUtils()
    london_time = time_utils.get_current_date_time()
    # Time slots generated from 9:00 AM to 7:00 PM in 30-minute intervals
    TIME_SLOTS = time_utils.generate_time_slots(time(9, 0), time(19, 0), 30)
    first_name = forms.CharField(max_length=41,
                                 min_length=3,
                                 widget=forms.widgets.TextInput
                                 (attrs={'placeholder': 'Enter Name...', 'class': 'form-control'}),
                                         label='Full Name')

    reservation_date = forms.DateField(label='Pick Date', widget=forms.widgets.DateInput(
        attrs={'type': 'date',
               'format':['%d-%m-%Y'],
               'value': london_time.date(),
               'class': 'form-control'}))

    reservation_slot = forms.ChoiceField(label='Select Time Slot', choices=TIME_SLOTS,
        widget=forms.Select(attrs={'type': 'time', 'class': 'form-control'}))
