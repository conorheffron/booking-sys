"""
booking-sys Views Mapping & Logic
"""
from django.urls import path
from hr.views import Views
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    path('csrf/', Views.csrf),

    path('version/', Views.version, name='version'),

    path('bookings', Views.table_view, name='bookings_by_date'),

    # Get or update a booking by ID (GET, PUT): /bookingsById/<reservation_id>
    path('bookingsById/<int:reservation_id>', Views.bookings_by_id, name='bookingsById'),

    path('reservations', Views.save_reservation, name='save_reservation'),
    path('reservations/edit/<int:reservation_id>/', Views.edit_reservation, name='edit_reservation')
]
