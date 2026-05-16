"""
booking-sys Views Mapping & Logic
"""
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from hr.views import (
    csrf_view,
    auth_status_view,
    login_view,
    logout_view,
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
    path('auth/status', auth_status_view, name='auth_status'),
    path('auth/login', login_view, name='login'),
    path('auth/logout', logout_view, name='logout'),

    path('version/', version_view, name='version'),

    path('bookings', table_view, name='bookings_by_date'),

    # Get, Delete or update a booking by ID (GET, PUT): /bookingsById/<reservation_id>
    path('bookingsById/<int:reservation_id>', bookings_by_id_view, name='bookingsById'),

    path('reservations', save_reservation_view, name='save_reservation'),
    path('reservations/edit/<int:reservation_id>/', Views.edit_reservation, name='edit_reservation')
]
