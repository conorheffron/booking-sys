"""booking-sys views Mapping & Logic
"""
import logging
from datetime import datetime, date as dt_date
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from hr.forms import EditReservationForm
from hr import VERSION
from .models import Reservation
from .time_utils import TimeUtils
import json

logger = logging.getLogger(__name__)

class Views():
    """Views class for Views Mapping & Logic
    """
    
    @classmethod
    def version(cls, request:WSGIRequest):
        """GET Application Version for current deployment
        Parameters
        ----------
        request : Requests
        """
        logger.info('Request information (%s)', request)
        app_version = VERSION
        logger.info('Application version (%s)', app_version)
        return HttpResponse(str(app_version))


    @classmethod
    def table_view(cls, request:WSGIRequest):
        """GET bookings by date request parameter
        Parameters
        ----------
        request : Requests
        """
        date = request.GET.get("date", TimeUtils.get_current_date_time().date())
        return cls.__find_bookings_by_date(cls, date)

    @classmethod
    def edit_reservation(cls, request, reservation_id):
        """
        Handle the editing of an existing reservation.

        This view allows users to update the reservation date and time slot for a given reservation.
        On GET requests, it displays a form pre-filled with the current reservation details.
        On POST requests, it validates and saves the new date and time slot, 
        ensuring no double-booking occurs.
        If the selected date and slot are already reserved by another booking, 
        an error is displayed.

        Parameters
        ----------
        request : HttpRequest
            The HTTP request object.
        reservation_id : int
            The ID of the reservation to be edited.

        Returns
        -------
        HttpResponse
            Renders the edit reservation form on GET or invalid POST, 
            or redirects to the reservations
            list on successful update.
        """
        reservation = get_object_or_404(Reservation, pk=reservation_id)
        if request.method == "POST":
            form = EditReservationForm(request.POST)
            if form.is_valid():
                reservation_date = form.cleaned_data['reservation_date']
                reservation_slot = form.cleaned_data['reservation_slot']

                # Prevent double-book
                if Reservation.objects.filter(
                    reservation_date=reservation_date,
                    reservation_slot=reservation_slot
                ).exclude(id=reservation_id).exists():
                    return render(request, "edit_reservation.html", {
                        "form": form,
                        "reservation": reservation,
                        "error": "Booking Failed: Already Reserved."
                    })

                reservation.reservation_date = reservation_date
                reservation.reservation_slot = reservation_slot
                reservation.save()
                return redirect("reservations")  # or return to reservations list
        else:
            form = EditReservationForm(initial={
                "reservation_date": reservation.reservation_date,
                "reservation_slot": reservation.reservation_slot
            })
        return render(request, "edit_reservation.html", {
            "form": form,
            "reservation": reservation
        })

    @classmethod
    def bookingsById(cls, request, reservation_id):
        """
        GET: Return booking info by id as JSON
        PUT: Update booking info by id from JSON body
        """
        reservation = get_object_or_404(Reservation, pk=reservation_id)

        if request.method == "GET":
            data = {
                "id": reservation.id,
                "first_name": reservation.first_name,
                "reservation_date": str(reservation.reservation_date),
                "reservation_slot": reservation.reservation_slot,
            }
            return JsonResponse(data, status=200)

        elif request.method == "PUT":
            try:
                body = json.loads(request.body.decode("utf-8"))
            except Exception:
                return JsonResponse({"error": "Invalid JSON body"}, status=400)

            reservation_date = body.get("reservation_date")
            reservation_slot = body.get("reservation_slot")
            first_name = body.get("first_name")

            # Validate input
            if not reservation_date or not reservation_slot or not first_name:
                return JsonResponse({"error": "All fields are required."}, status=400)

            # Convert "02:00 PM" to "14:00"
            try:
                from datetime import datetime
                slot_time = datetime.strptime(reservation_slot, "%I:%M %p").time()
            except Exception:
                return JsonResponse({"error": "Invalid time format for reservation_slot."}, status=400)

            # Prevent double-booking (exclude current reservation)
            if Reservation.objects.filter(
                reservation_date=reservation_date,
                reservation_slot=slot_time
            ).exclude(pk=reservation_id).exists():
                return JsonResponse({"error": "Booking Failed: Already Reserved."}, status=400)

            reservation.first_name = first_name
            reservation.reservation_date = reservation_date
            reservation.reservation_slot = slot_time
            reservation.save()

            data = {
                "id": reservation.id,
                "first_name": reservation.first_name,
                "reservation_date": str(reservation.reservation_date),
                "reservation_slot": reservation.reservation_slot.strftime("%I:%M %p"),  # return in 12hr format
                "success": True
            }
            return JsonResponse(data, status=200)
        else:
            return JsonResponse({"error": "Method not allowed."}, status=405)
        

    @classmethod
    def save_reservation(cls, request):
        """
        Handle saving (creating or updating) a reservation via PUT.
        """
        if request.method != "PUT":
            return JsonResponse({"error": "Method not allowed."}, status=405)

        try:
            body = json.loads(request.body.decode("utf-8"))
        except Exception:
            return JsonResponse({"error": "Invalid JSON body"}, status=400)

        first_name = body.get("first_name")
        reservation_date = body.get("reservation_date")
        reservation_slot = body.get("reservation_slot")

        if not first_name or not reservation_date or not reservation_slot:
            return JsonResponse({"error": "All fields are required."}, status=400)

        # Convert time string like "02:00 PM" to time object
        try:
            slot_time = datetime.strptime(reservation_slot, "%I:%M %p").time()
        except Exception:
            return JsonResponse({"error": "reservation_slot must be in format HH:MM AM/PM"}, status=400)

        # Prevent double booking
        if Reservation.objects.filter(
            reservation_date=reservation_date,
            reservation_slot=slot_time
        ).exists():
            return JsonResponse({"error": "Booking Failed: Already Reserved."}, status=400)

        # Save reservation
        reservation = Reservation.objects.create(
            first_name=first_name,
            reservation_date=reservation_date,
            reservation_slot=slot_time
        )

        data = {
            "id": reservation.id,
            "first_name": reservation.first_name,
            "reservation_date": str(reservation.reservation_date),
            "reservation_slot": reservation.reservation_slot.strftime("%I:%M %p"),
            "success": True
        }
        return JsonResponse(data, status=201)
    
    def __find_bookings_by_date(self, date):
        """Bookings by date and return JSON 
        response (private method)
        Parameters
        ----------
        date: The date in format %y-%m-%d i.e. 2024-09-07
        """
        today = dt_date.today()
        queryset = None

        try:
            # Try to parse provided date
            query_date = datetime.strptime(date, "%Y-%m-%d").date()
            # If successful, filter by that date
            queryset = Reservation.objects.order_by('reservation_slot').filter(reservation_date=query_date)
            logger.info('GET by date (%s) Query set results: %s', query_date, list(queryset.values('id', 'first_name', 'reservation_date', 'reservation_slot')))
        except (TypeError, ValueError):
            # If date is None or invalid, show all bookings after today
            queryset = Reservation.objects.order_by('reservation_slot').filter(reservation_date__gt=today)
            logger.info('GET by future date (after %s) Query set results: %s', today, list(queryset.values('id', 'first_name', 'reservation_date', 'reservation_slot')))

        data = list(queryset.values('id', 'first_name', 'reservation_date', 'reservation_slot'))

        return JsonResponse({
            'message': 'success',
            'reservations': data
        })
