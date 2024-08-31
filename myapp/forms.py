from django import forms

# ModelForm: MenuForm
class ReservationForm(forms.Form):
    first_name = forms.CharField(max_length = 20)
    reservation_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    reservation_slot = forms.TimeField(widget=forms.widgets.TimeInput(attrs={'type': 'time'}))

