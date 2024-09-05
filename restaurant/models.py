"""
Reservation Form Module
"""
from django.db import models

# Reservation model
class Reservation(models.Model):
    first_name = models.CharField(max_length = 30)
    reservation_date = models.DateField()
    reservation_slot = models.TimeField()
    