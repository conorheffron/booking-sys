from . import views
from django.urls import path

urlpatterns = [
    path('', views.form_view, name="home"),
    path('book/', views.form_view, name="book"),
    path('reservations/', views.reservations_view, name="reservations"),
    path('bookings', views.table_view, name='bookings_by_date'),
]