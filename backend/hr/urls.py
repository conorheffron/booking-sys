"""
booking-sys Views Mapping & Logic
"""
from django.urls import path
from hr.views import Views

urlpatterns = [
    path('version/', Views.version, name='version'),

    path('bookings/<str:date>', Views.tableView, name='bookings_by_date_api'),
    path('bookings', Views.tableView, name='all_bookings'),

    # Get or update a booking by ID (GET, PUT): /bookingsById/<reservation_id>
    path('bookingsById/<int:reservation_id>', Views.bookingsById, name='bookingsById'),

    path('reservations', Views.saveReservation, name='save_reservation'),
    path('reservations/edit/<int:reservation_id>/', Views.editReservation, name='edit_reservation')
]
