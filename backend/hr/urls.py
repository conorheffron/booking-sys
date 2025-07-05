"""
booking-sys Views Mapping & Logic
"""
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from hr.views import (
    csrf_view,
    version_view,
    table_view,
    bookings_by_id_view,
    save_reservation_view,
    Views
)

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('csrf/', csrf_view),

    path('version/', version_view, name='version'),

    path('bookings', table_view, name='bookings_by_date'),

    # Get, Delete or update a booking by ID (GET, PUT): /bookingsById/<reservation_id>
    path('bookingsById/<int:reservation_id>', bookings_by_id_view, name='bookingsById'),

    path('reservations', save_reservation_view, name='save_reservation'),
    path('reservations/edit/<int:reservation_id>/', Views.edit_reservation, name='edit_reservation')
]
