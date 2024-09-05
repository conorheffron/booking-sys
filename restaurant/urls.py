"""
littlelemon Views Mapping & Logic
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.form_view, name="home"),
    path('book/', views.form_view, name="book"),
    path('reservations/', views.reservations_view, name="reservations"),
    path('bookings/<str:date>/', views.bookings_view, name='bookings_by_date'),
    path('bookings', views.table_view, name='bookings_by_date')
]
