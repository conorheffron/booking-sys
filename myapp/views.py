from django.shortcuts import render
from myapp.forms import ReservationForm
from .models import Reservation
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

def table_view(request, date):
    logger.inf(date);
    reservations =  Reservation.objects.all()
    logger.info(reservations)
    return JsonResponse({
                'message': 'success',
                'reservations': reservations
            })

def reservations_view(request):
    reservations =  Reservation.objects.all()
    logger.info(reservations)
    return render(request, 'reservations.html', {'reservations': reservations})

def form_view(request):
    form = ReservationForm()
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        logger.info(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            booking_date = cd['reservation_date']
            
            lf = Reservation(
                first_name = cd['first_name'],
                reservation_date = booking_date,
                reservation_slot = cd['reservation_slot'],
            )

            lf.save()

            reservations_by_date = Reservation.objects.filter(reservation_date=booking_date)
            logger.info(reservations_by_date)
            data = list(reservations_by_date.values('first_name', 'reservation_date', 'reservation_slot'))
            return JsonResponse({
                'message': 'success',
                'reservations': data
            })
    reservations =  Reservation.objects.all()
    logger.info(reservations)
    return render(request, 'booking.html', {'form': form, 'reservations': reservations})