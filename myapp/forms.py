from django import forms
from datetime import datetime

# ModelForm: ReservationForm
class ReservationForm(forms.Form):
    first_name = forms.CharField(max_length = 20)
    reservation_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date', 'value': datetime.now().date()}))
    reservation_slot = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type': 'time'}))

