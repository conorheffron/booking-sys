"""
Reservation Models Module
"""
from django.db import models


# Reservation Form Module
class Reservation(models.Model):
    """A DB Model to save a reservation/booking.
    Attributes:
        first_name  The first name against the reservation.
        reservation_date  The booking date.
        reservation_slot The booking time slot (HH:MM:SS).
    """
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length = 30)
    reservation_date = models.DateField()
    reservation_slot = models.TimeField()
