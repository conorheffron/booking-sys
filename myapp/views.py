from django.shortcuts import render
from myapp.forms import ReservationForm
from .models import Reservation
from django.http import JsonResponse

def form_view(request):
    form = ReservationForm()
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        print(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            
            lf = Reservation(
                first_name = cd['first_name'],
                reservation_date = cd['reservation_date'],
                reservation_slot = cd['reservation_slot'],
            )
            
            lf.save()
            return JsonResponse({
                'message': 'success'
            })
    return render(request, 'booking.html', {'form': form})