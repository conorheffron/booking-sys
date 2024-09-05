"""littlelemon Views Mapping & Logic
"""
from .models import Reservation
from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render
import logging
from restaurant.forms import ReservationForm


logger = logging.getLogger(__name__)


# GET bookings by date request parameter
def table_view(request):
    date = request.GET.get("date", datetime.today().date())
    return findBookingsByDate(date)


# GET bookings by date request path variable
def bookings_view(request, date):
    return findBookingsByDate(date)


# GET bookings by date JSON response
def findBookingsByDate(date):
    reservations_by_date = Reservation.objects.filter(reservation_date=date)
    
    data = list(reservations_by_date.values('first_name', 'reservation_date', 'reservation_slot'))
    logger.info(f'GET by date ({date}) Query set results: {data}')
    return JsonResponse({
        'message': 'success',
        'reservations': data
    })


# Resolve all reservations view 7 data request
def reservations_view(request):
    data =  list(Reservation.objects.all().values('first_name', 'reservation_date', 'reservation_slot'))
    logger.info(f'GET All Query set results: {data}')
    return render(request, 'reservations.html', {'reservations': data})


# Resolve make a reservation form submit
def form_view(request):
    form = ReservationForm()
    
    #  POST request logic
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        logger.info(request.POST)
        if form.is_valid():
            # clean & extract form data
            cd = form.cleaned_data

            booking_date = cd['reservation_date']
            booking_slot = cd['reservation_slot']

            # booking flow logic
            reservations_by_date = Reservation.objects.filter(reservation_date=booking_date, reservation_slot=booking_slot)
            message = ''
            if reservations_by_date.exists():
                message = 'Booking Failed - Already Reserved'
            else:
                # map form object to model & save to DB
                reservation = Reservation(
                    first_name = cd['first_name'],
                    reservation_date = booking_date,
                    reservation_slot = booking_slot,
                )
                reservation.save()
                message = 'Booking Complete'
            
            # POST response JSON
            data = list(Reservation.objects.filter(reservation_date=booking_date).values('first_name', 'reservation_date', 'reservation_slot'))
            logger.info(f'POST Query set results: {data}')
            return JsonResponse({
                'message': message,
                'reservations': data
                })
    else:
        # GET Response logic
        reservations =  Reservation.objects.all()
        data = list(reservations.values_list('first_name', 'reservation_date', 'reservation_slot'))
        logger.info(f'GET Query set results: {data}')
        return render(request, 'booking.html', {'form': form, 'reservations': reservations})
