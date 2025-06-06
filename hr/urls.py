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
    path('version/', Views.version, name='version'),
    path('bookings', Views.table_view, name='bookings_by_date'),
    path('reservations/edit/<int:reservation_id>/', Views.edit_reservation, name='edit_reservation')
]
