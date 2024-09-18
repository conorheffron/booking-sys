"""
Reservation Form Module
"""
from datetime import datetime
import pytz
from django import forms

class ReservationForm(forms.Form):
    """A Form to make a reservation/booking.
    Attributes:
        first_name  The first name against the reservation.
        reservation_date  The booking date.
        reservation_slot The booking time slot (HH:MM:SS).
    """
    tz = pytz.timezone('UTC')
    tz_time = tz.localize(datetime.now())
    london_tz = pytz.timezone('Europe/London')
    london_time = tz_time.astimezone(london_tz)

    first_name = forms.CharField(max_length=15,
                                 min_length=3,
                                 widget=forms.widgets.TextInput
                                 (attrs={'style': 'width:45%',
                                         'placeholder': 'Enter Name...'}), 
                                         label='')

    reservation_date = forms.DateField(label='', widget=forms.widgets.DateInput(
        attrs={'type': 'date',
               'format':['%d-%m-%Y'],
               'value': london_time.date(),
               'style': 'width:45%'}))

    reservation_slot = forms.TimeField(label='', widget=forms.widgets.TimeInput(
        attrs={'type': 'time',
               'format':['HH:mm'],
               'value': london_time.strftime('%H:%M'),
               'style': 'width:45%'}))
