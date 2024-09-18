"""booking-sys views Mapping & Logic
"""
from datetime import datetime
import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from restaurant.forms import ReservationForm
from .models import Reservation

logger = logging.getLogger(__name__)

class Views(object):
    """Views class for Views Mapping & Logic
    """

    @classmethod
    def table_view(cls, request:WSGIRequest):
        """GET bookings by date request parameter
        Parameters
        ----------
        request : Requests
        """
        date = request.GET.get("date", datetime.today().date())
        return cls.__find_bookings_by_date(cls, date)

    @classmethod
    def bookings_view(cls, request:WSGIRequest, date):
        """GET bookings by date request path variable
        Parameters
        ----------
        request : Requests
        date: The date in format %y-%m-%d i.e. 2024-09-07
        """
        logger.info('Request information (%s)', request)
        return cls.__find_bookings_by_date(cls, date)

    @classmethod
    def reservations_view(cls, request:WSGIRequest):
        """Resolve all reservations view data request
        Parameters
        ----------
        request : Requests
        """
        data =  list(Reservation.objects.all().values(
            'first_name', 'reservation_date', 'reservation_slot'))
        logger.info('GET All Query set results: %s', data)
        return render(request, 'reservations.html', {'reservations': data})

    @classmethod
    def form_view(cls, request:WSGIRequest):
        """Resolve make a reservation form submit
        Parameters
        ----------
        request : Requests
        """
        form = ReservationForm()
        #  POST request logic
        if request.method == 'POST':
            form = ReservationForm(request.POST)
            logger.info(request.POST)
            if form.is_valid():
                # clean & extract form data
                form_data = form.cleaned_data
                booking_date = form_data['reservation_date']
                booking_slot = form_data['reservation_slot']

                # booking flow logic
                reservations_by_date = Reservation.objects.filter(
                    reservation_date=booking_date, reservation_slot=booking_slot)
                message = ''
                if reservations_by_date.exists():
                    message = 'Booking Failed - Already Reserved'
                else:
                    # map form object to model & save to DB
                    reservation = Reservation(
                        first_name = form_data['first_name'],
                        reservation_date = booking_date,
                        reservation_slot = booking_slot,
                    )
                    reservation.save()
                    message = 'Booking Complete'
                # POST response JSON
                data = list(Reservation.objects.filter(reservation_date=booking_date).values(
                    'first_name', 'reservation_date', 'reservation_slot'))
                logger.info('POST Query set results: %s', data)
                return JsonResponse({
                    'message': message,
                    'reservations': data
                    })
        else:
            # Bookings view default logic
            reservations =  Reservation.objects.all()
            data = list(reservations.values_list('first_name', 'reservation_date', 'reservation_slot'))
            logger.info('GET Query set results: %s', data)
            return render(request, 'booking.html', {'form': form, 'reservations': reservations})
        
    def __find_bookings_by_date(self, date):
        """Bookings by date and return JSON response (private method)
        Parameters
        ----------
        date: The date in format %y-%m-%d i.e. 2024-09-07
        """
        reservations_by_date = Reservation.objects.filter(reservation_date=date)
        data = list(reservations_by_date.values('first_name', 'reservation_date', 'reservation_slot'))
        logger.info('GET by date (%s) Query set results: %s', date, data)
        return JsonResponse({
            'message': 'success',
            'reservations': data
        })
