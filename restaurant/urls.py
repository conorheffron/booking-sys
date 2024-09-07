"""
littlelemon Views Mapping & Logic
"""
from django.urls import path, re_path
from django.http import HttpResponse
from restaurant import views

handler404 = views.handler404

urlpatterns = [
    path('', views.form_view, name="home"),
    path('book/', views.form_view, name="book"),
    path('reservations/', views.reservations_view, name="reservations"),
    path('bookings/<str:date>/', views.bookings_view, name='bookings_by_date'),
    path('bookings', views.table_view, name='bookings_by_date'),
    re_path(r'.*', handler404)
]
