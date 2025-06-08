"""
booking-sys Views Mapping & Logic
"""
from django.urls import path
from hr.views import Views

urlpatterns = [
    path('', Views.form_view, name="home"),
    path('book/', Views.form_view, name="book"),
    path('reservations/', Views.reservations_view, name="reservations"),
    path('bookings/<str:date>/', Views.bookings_view, name='bookings_by_date'),
    path('api/version/', Views.version, name='version'),
    path('api/bookings/<str:date>', Views.table_view, name='bookings_by_date_api'),
    path('api/bookings', Views.table_view, name='all_bookings'),
    # Get or update a booking by ID (GET, PUT): /bookingsById/<reservation_id>
    path('api/bookingsById/<int:reservation_id>', Views.bookingsById, name='bookingsById'),
    path('api/reservations', Views.save_reservation, name='save_reservation'),
    path('api/reservations/edit/<int:reservation_id>/', Views.edit_reservation, name='edit_reservation')
]
