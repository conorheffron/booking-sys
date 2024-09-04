from django.test import TestCase 
from .models import Reservation
from .forms import ReservationForm
from datetime import datetime

class RestaurantTests(TestCase):

    def setUp(self):
        pass

    def test_create_booking(self):
        # given
        now = datetime.now()
        fname = "Conor"
        booking_date = now.strptime('01/08/2015','%d/%m/%Y').date()
        booking_slot = now.strftime("%H:%M:%S")


        # when
        result = Reservation.objects.create(first_name=fname, 
                                             reservation_date=booking_date, 
                                             reservation_slot=booking_slot)
        
        # then
        self.assertEqual(result.first_name, fname)
        self.assertEqual(result.reservation_date, booking_date)
        self.assertEqual(result.reservation_slot, booking_slot)

    def test_populate_form(self):
        # given
        now = datetime.now()
        fname = "Conor"
        booking_date = '01/11/2020'
        booking_slot = '01:01:01'
        form_data = {"first_name": fname, "reservation_date": booking_date, "reservation_slot": booking_slot}

        # when
        result = ReservationForm(data=form_data)
        
        # then
        self.assertTrue(result.is_valid())
        self.assertEqual(result.__dict__['data']["first_name"], "Conor")
        self.assertEqual(result.__dict__['data']["reservation_date"], booking_date)
        self.assertEqual(result.__dict__['data']["reservation_slot"], booking_slot)
