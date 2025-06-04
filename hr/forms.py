"""
Reservation Form Module
"""
from django import forms
from .time_utils import TimeUtils
from datetime import datetime, timedelta, time

class ReservationForm(forms.Form):
    """A Form to make a reservation/booking.
    Attributes:
        first_name  The first name against the reservation.
        reservation_date  The booking date.
        reservation_slot The booking time slot (HH:MM).
    """
    time_utils = TimeUtils()
    london_time = time_utils.get_current_date_time()
    TIME_SLOTS = time_utils.generate_time_slots(time(9, 0), time(17, 0), 30)  # 9:00 AM to 7:00 PM, 30-minute intervals

    first_name = forms.CharField(max_length=15,
                                 min_length=3,
                                 widget=forms.widgets.TextInput
                                 (attrs={'style': 'width:50%',
                                         'placeholder': 'Enter Name...'}), 
                                         label='')

    reservation_date = forms.DateField(label='', widget=forms.widgets.DateInput(
        attrs={'type': 'date',
               'format':['%d-%m-%Y'],
               'value': london_time.date(),
               'style': 'width:50%'}))

    reservation_slot = forms.ChoiceField(choices=TIME_SLOTS, label="Select a Time Slot")
