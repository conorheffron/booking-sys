from . import views
from django.urls import path

urlpatterns = [
    path('', views.form_view, name="home"),
    path('reservations/', views.reservations_view, name="reservations"),
    path('bookings/<str:date>/', views.table_view, name='bookings_by_date'),
]