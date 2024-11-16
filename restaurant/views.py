"""booking-sys views Mapping & Logic
"""
from datetime import datetime
import logging
from django.http import JsonResponse
from django.shortcuts import render
from django.core.handlers.wsgi import WSGIRequest
from restaurant.forms import ReservationForm
from .models import Reservation
from .time_utils import TimeUtils

logger = logging.getLogger(__name__)

class Views():
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
        # get current date/ time
        london_date_time = TimeUtils().get_current_date_time()
        # get all active reservations (after current date/time)
        data =  list(Reservation.objects.filter(reservation_date__gte=london_date_time.date(),
                     reservation_slot__gte=london_date_time.strftime("%H:%M:%S"))
                     .order_by('-reservation_date', '-reservation_slot')
                     .values('id', 'first_name', 'reservation_date', 'reservation_slot'))
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
                # get current date/ time for in-past validation
                london_date_time = TimeUtils().get_current_date_time()

                # build JSON response
                message = ''
                if ((booking_date < london_date_time.date()) or
                    (london_date_time.date() == booking_date
                     and booking_slot <= london_date_time.time())):
                    message = 'Booking Failed: Date/Time is in the past.'
                elif reservations_by_date.exists():
                    message = 'Booking Failed: Already Reserved.'
                else:
                    # map form object to model & save to DB
                    reservation = Reservation(
                        first_name = form_data['first_name'],
                        reservation_date = booking_date,
                        reservation_slot = booking_slot,
                    )
                    reservation.save()
                    message = f'Booking Complete: Confirmed for {booking_date} at {booking_slot}'
                # POST response JSON
                data = list(Reservation.objects
                            .order_by('-reservation_slot')
                            .filter(reservation_date=booking_date)
                            .values('id', 'first_name', 'reservation_date', 'reservation_slot'))
                logger.info('POST Query set results: %s', data)
                return JsonResponse({
                    'message': message,
                    'reservations': data
                    })
        else:
            # Bookings view default logic
            reservations = Reservation.objects.all()
            data = list(reservations.values_list('id',
                                                 'first_name',
                                                 'reservation_date',
                                                 'reservation_slot'))
            logger.info('GET Query set results: %s', data)
            return render(request, 'booking.html', {'form': form,
                                                    'reservations': reservations})

    def __find_bookings_by_date(self, date):
        """Bookings by date and return JSON 
        response (private method)
        Parameters
        ----------
        date: The date in format %y-%m-%d i.e. 2024-09-07
        """
        reservations_by_date = Reservation.objects.order_by(
            '-reservation_slot').filter(
                reservation_date=date)
        data = list(reservations_by_date.values('id',
                                                'first_name',
                                                'reservation_date',
                                                'reservation_slot'))
        logger.info('GET by date (%s) Query set results: %s', date, data)
        return JsonResponse({
            'message': 'success',
            'reservations': data
        })
