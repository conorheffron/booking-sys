"""
booking-sys Views Mapping & Logic
"""
from django.urls import path
from hr.views import Views

urlpatterns = [
    path('csrf/', Views.csrf),

    path('version/', Views.version, name='version'),

    path('bookings/<str:date>', Views.table_view, name='bookings_by_date_api'),
    path('bookings', Views.table_view, name='all_bookings'),

    # Get or update a booking by ID (GET, PUT): /bookingsById/<reservation_id>
    path('bookingsById/<int:reservation_id>', Views.bookings_by_id, name='bookingsById'),

    path('reservations', Views.save_reservation, name='save_reservation'),
    path('reservations/edit/<int:reservation_id>/', Views.edit_reservation, name='edit_reservation')
]

