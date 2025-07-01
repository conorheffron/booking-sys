"""booking-sys views Mapping & Logic
"""
import logging
from datetime import datetime, date as dt_date, time as dt_time
import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.handlers.wsgi import WSGIRequest

from rest_framework.decorators import api_view
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    OpenApiTypes,
    extend_schema_view
)

from hr.forms import EditReservationForm
from hr import VERSION
from .models import Reservation
from .time_utils import TimeUtils

logger = logging.getLogger(__name__)

class Views:
    """Views class for Views Mapping & Logic
    """
    @classmethod
    def csrf(cls, request:WSGIRequest):
        """GET CSRF Token / Cookie Value from incoming requests"""
        return JsonResponse({'csrfToken': request.META.get('CSRF_COOKIE', '')})

    @classmethod
    def version(cls, request:WSGIRequest):
        """GET Application Version for current deployment"""
        logger.info('Request information (%s)', request)
        app_version = VERSION
        logger.info('Application version (%s)', app_version)
        return HttpResponse(str(app_version))

    @classmethod
    def table_view(cls, request):
        """GET bookings by date request parameter"""
        date = request.GET.get("date", TimeUtils.get_current_date_time().date())
        return cls._find_bookings_by_date(cls, date)

    @classmethod
    def edit_reservation(cls, request, reservation_id):
        """
        Handle the editing of an existing reservation.
        Do not allow editing of past bookings.
        """
        reservation = get_object_or_404(Reservation, pk=reservation_id)

        # Block editing of past bookings
        now = datetime.now()
        # Combine date and time for comparison
        reservation_datetime = datetime.combine(reservation.reservation_date,
                                               reservation.reservation_slot)
        if reservation_datetime < now:
            return render(request, "edit_reservation.html", {
                "form": None,
                "reservation": reservation,
                "error": "Editing past bookings is not allowed."
            })

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

                # Prevent editing to a past date/time
                new_datetime = datetime.combine(reservation_date, reservation_slot)
                if new_datetime < now:
                    return render(request, "edit_reservation.html", {
                        "form": form,
                        "reservation": reservation,
                        "error": "You cannot update a reservation to a past date/time."
                    })

                reservation.reservation_date = reservation_date
                reservation.reservation_slot = reservation_slot
                reservation.save()
                return redirect("reservations")
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
    def bookings_by_id(cls, request, reservation_id):
        """
        GET: Return booking info by id as JSON
        PUT: Update booking info by id from JSON body
        - Do not allow editing of past bookings
        - Do not allow updating to a past date/time
        """
        reservation = get_object_or_404(Reservation, pk=reservation_id)

        if request.method == "GET":
            data = {
                "id": reservation.id,
                "first_name": reservation.first_name,
                "reservation_date": str(reservation.reservation_date),
                "reservation_slot": reservation.reservation_slot.strftime("%I:%M %p") 
                if isinstance(reservation.reservation_slot, dt_time)
                else str(reservation.reservation_slot),
            }
            return JsonResponse(data, status=200)
        elif request.method == "PUT":
            now = datetime.now()
            # Block editing of past bookings
            original_datetime = datetime.combine(reservation.reservation_date,
                                                 reservation.reservation_slot)
            if original_datetime < now:
                return JsonResponse({"error": "Editing past bookings is not allowed."},
                                    status=400)
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
                slot_time = datetime.strptime(reservation_slot, "%I:%M %p").time()
            except Exception:
                return JsonResponse(
                    {
                        "error": "Invalid time format for reservation_slot."
                        },
                        status=400)

            # Prevent double-booking (exclude current reservation)
            if Reservation.objects.filter(
                reservation_date=reservation_date,
                reservation_slot=slot_time
            ).exclude(pk=reservation_id).exists():
                return JsonResponse({"error": "Booking Failed: Already Reserved."}, status=400)

            # Prevent updating reservation to a past date/time
            try:
                new_datetime = datetime.combine(
                    datetime.strptime(reservation_date, "%Y-%m-%d").date(),
                    slot_time
                )
            except Exception:
                return JsonResponse({
                    "error": "Invalid reservation_date or reservation_slot."
                    }, status=400)
            if new_datetime < now:
                return JsonResponse({
                    "error": "Cannot update reservation to a past date/time."
                    }, status=400)

            reservation.first_name = first_name
            reservation.reservation_date = reservation_date
            reservation.reservation_slot = slot_time
            reservation.save()

            data = {
                "id": reservation.id,
                "first_name": reservation.first_name,
                "reservation_date": str(reservation.reservation_date),
                "reservation_slot": reservation.reservation_slot.strftime("%I:%M %p"),
                "success": True
            }
            return JsonResponse(data, status=200)
        else:
            return JsonResponse({"error": "Method not allowed."}, status=405)

    @classmethod
    def save_reservation(cls, request):
        """
        Handle saving (creating or updating) a reservation via PUT.
        Do not allow new reservations for past date/time.
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
            return JsonResponse({"error": "reservation_slot must be in format HH:MM AM/PM"},
                                status=400)

        # Prevent reservation for past date/time
        try:
            reservation_datetime = datetime.combine(
                datetime.strptime(reservation_date, "%Y-%m-%d").date(),
                slot_time
            )
        except Exception:
            return JsonResponse({"error": "Invalid reservation_date or reservation_slot."},
                                status=400)
        now = datetime.now()
        if reservation_datetime < now:
            return JsonResponse({"error": "Cannot make a reservation for a past date/time."},
                                status=400)

        # Prevent double booking
        if Reservation.objects.filter(
            reservation_date=reservation_date,
            reservation_slot=slot_time
        ).exists():
            return JsonResponse({"error": "Booking Failed: Already Reserved."},
                                status=400)

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

    def _find_bookings_by_date(self, date):
        """Bookings by date and return JSON response (private method)"""
        today = dt_date.today()
        queryset = None

        try:
            query_date = datetime.strptime(date, "%Y-%m-%d").date()
            # Order by reservation_date DESC, reservation_slot DESC for most recent to top
            queryset = Reservation.objects.filter(
                reservation_date=query_date
            ).order_by('-reservation_date', '-reservation_slot')
            logger.info('GET by date (%s) Query set results: %s',
                        query_date,
                        list(queryset.values('id',
                                             'first_name',
                                             'reservation_date',
                                             'reservation_slot')))
        except (TypeError, ValueError):
            queryset = Reservation.objects.filter(
                reservation_date__gt=today
            ).order_by('-reservation_date', '-reservation_slot')
            logger.info('GET by future date (after %s) Query set results: %s',
                        today,
                        list(queryset.values('id',
                                             'first_name',
                                             'reservation_date',
                                             'reservation_slot')))
        data = list(queryset.values('id', 'first_name', 'reservation_date', 'reservation_slot'))
        return JsonResponse({
            'message': 'success',
            'reservations': data
        })

# ==== WRAPPER VIEWS FOR DRF SPECTACULAR + Django URLS ====

@extend_schema(
    methods=["GET"],
    description="GET CSRF Token / Cookie Value from incoming requests",
    responses={200: OpenApiTypes.OBJECT}
)
@api_view(['GET'])
def csrf_view(request):
    return Views.csrf(request)

@extend_schema(
    methods=["GET"],
    description="GET Application Version for current deployment",
    responses={200: OpenApiTypes.STR}
)
@api_view(['GET'])
def version_view(request):
    return Views.version(request)

@extend_schema(
    methods=["GET"],
    description="GET bookings by date request parameter",
    parameters=[
        OpenApiParameter(
            name="date",
            type=OpenApiTypes.DATE,
            required=False,
            location=OpenApiParameter.QUERY,
            description="Filter bookings by date (YYYY-MM-DD)"
        )
    ],
    responses={200: OpenApiTypes.OBJECT}
)
@api_view(['GET'])
def table_view(request):
    return Views.table_view(request)

@extend_schema_view(
    get=extend_schema(
        description="GET: Return booking info by id as JSON",
        parameters=[
            OpenApiParameter(
                name="reservation_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="Reservation ID"
            )
        ],
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT}
    ),
    put=extend_schema(exclude=True)  # <--- this hides PUT in Swagger!
)
@api_view(['GET', 'PUT'])
def bookings_by_id_view(request, reservation_id):
    return Views.bookings_by_id(request, reservation_id)

@extend_schema(exclude=True)
@api_view(['PUT'])
def save_reservation_view(request):
    return Views.save_reservation(request)
