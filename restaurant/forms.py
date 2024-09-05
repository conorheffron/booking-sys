"""
Reservation Form Module
"""
from datetime import datetime
from django import forms


# ModelForm: ReservationForm Class and fields
class ReservationForm(forms.Form):

    first_name = forms.CharField(min_length=3, max_length = 15)
    reservation_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date', 'format':['%d-%m-%Y'], 'value': datetime.now().date()}))
    reservation_slot = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type': 'time'}))

