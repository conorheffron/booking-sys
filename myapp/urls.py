from . import views
from django.urls import path

urlpatterns = [
    path('', views.form_view, name="home"),
    path('bookings', views.table_view, name="bookings"),
]