"""
HR Tests Suite
"""
from datetime import date, time, datetime, timedelta
import json
import re
import pytest
from django.urls import reverse
from django.test import TestCase, RequestFactory
from django.core.exceptions import ValidationError
from .models import Reservation
from .forms import ReservationForm
from .time_utils import TimeUtils
from .views import Views

# HR Tests
@pytest.mark.django_db
class HrTests(TestCase):
    """HR Test cases
    """
    def setUp(self):
        self.factory = RequestFactory()
        self.reservation = Reservation.objects.create(
            first_name="Alice",
            reservation_date=date.today() + timedelta(days=1),
            reservation_slot=time(10, 0)
        )

    def test_create_booking(self):
        """HR Test case test_create_booking
        Parameters
        ----------
        self : TestCase
        """
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
        """HR Test case test_populate_form
        Parameters
        ----------
        self : TestCase
        """
        # given
        fname = "Conor"
        booking_date = '01/11/2020'
        booking_slot = '11:30'
        form_data = {"first_name": fname,
                     "reservation_date": booking_date,
                     "reservation_slot": booking_slot}
        # when
        result = ReservationForm(data=form_data)

        # then
        self.assertTrue(result.is_valid())
        self.assertEqual(result.__dict__['data']["first_name"], "Conor")
        self.assertEqual(result.__dict__['data']["reservation_date"], booking_date)
        self.assertEqual(result.__dict__['data']["reservation_slot"], booking_slot)

    def test_reservations_view_success(self):
        """HR Test case test_reservations_view_success
        Parameters
        ----------
        self : TestCase
        """
        # when
        response = self.client.get('/reservations/')

        # then
        self.assertContains(response, '<h3>All Active Reservations</h3>' + 
                                '\n        ' + 
                                '<table>\n            ' + 
                                    '<tr> \n                ' + 
                                        '<th>#</th>\n                ' + 
                                        '<th>Name</th>\n                ' + 
                                        '<th>Booking Date</th>\n                ' + 
                                        '<th>Booking time</th>\n            ' + 
                                    '</tr>\n            \n            ' + 
                                    '<tr> \n                ' + 
                                        '<td>1</td>\n                ' + 
                                        '<td>Alice</td>\n                ' + 
                                        '<td>2025-06-06</td>\n                ' + 
                                        '<td>10:00:00</td>\n                ' + 
                                    '<td>\n                    ' + 
                                        '<a href="/reservations/edit/1/" ' + 
                                        'class="btn btn-sm btn-warning">' + 
                                        'Edit</a>\n                ' + 
                                    '</td>\n            ' + 
                                    '</tr>\n            \n        ' + 
                                '</table>\n        <br />\n        ' + 
                                '<button type="button" class="btn btn-primary" ' + 
                                        'onClick="refresh()">Refresh</button>\n    ' + 
                            '</div>\n<body>', 
                            status_code=200)
        self.assertTemplateUsed(response, 'reservations.html')

    def test_bookings_by_date_request_param_success(self):
        """HR Test case test_bookings_by_date_request_param_success
        Parameters
        ----------
        self : TestCase
        """
        # when
        response = self.client.get('/bookings?date=2024-09-18')

        # then
        self.assertContains(response, json.dumps({"message": "success", "reservations": []}),
                            status_code=200)

    def test_bookings_by_date_request_param_fail(self):
        """HR Test case test_bookings_by_date_request_param_fail
        Parameters
        ----------
        self : TestCase
        """
        # when / then
        with self.assertRaisesMessage(ValidationError,
                                 '“2024-0918” value has an invalid date format. ' +
                                 'It must be in YYYY-MM-DD format.'):
            self.client.get('/bookings?date=2024-0918')

    def test_bookings_by_date_path_var_success(self):
        """HR Test case test_bookings_by_date_path_var_success
        Parameters
        ----------
        self : TestCase
        """
        # when
        response = self.client.get('/bookings/2024-09-18/')

        # then
        self.assertContains(response, '', status_code=200)

    def test_home_page_success(self):
        """HR Test case test_home_page_success
        Parameters
        ----------
        self : TestCase
        """
        # when
        response = self.client.get('/book/')

        # then
        self.assertContains(response, '\n        <h3>Bookings by Date</h3>\n        <table>\n' +
                            '            <tbody id="tableData"></tbody>\n        </table>\n    ' +
                            '</div>\n    \n</body>\n</html>', 
                            status_code=200 )
        self.assertTemplateUsed(response, 'booking.html')

    def test_booking_success(self):
        """HR Test case test_booking_success
        Parameters
        ----------
        self : TestCase
        """
        # given
        test_name = 'Conor'
        current_date_time = TimeUtils().get_current_date_time() + timedelta(days=1)
        test_date = current_date_time.strftime('%Y-%m-%d')
        test_time = '09:30'

        # when
        response = self.client.post('/book/', data={'first_name': test_name,
                                                    'reservation_date': test_date,
                                                    'reservation_slot': test_time})

        # then
        self.assertContains(response, json.dumps({"message":
                                                  "Booking Complete: Confirmed for " +
                                                  f"{test_date} at {test_time}:00",
                                                  "reservations": [{
                                                      "id": 2,
                                                      "first_name": test_name,
                                                      "reservation_date": test_date,
                                                      "reservation_slot": test_time + ':00'},
                                                      {"id": 1,
                                                       "first_name": "Alice",
                                                       "reservation_date": "2025-06-06",
                                                       "reservation_slot": "10:00:00"}]}),
                                                      status_code=200)

    def test_booking_in_past_fail(self):
        """HR Test case test_booking_in_past_fail
        Parameters
        ----------
        self : TestCase
        """
        # given
        test_name = 'Sade'
        current_date_time = TimeUtils().get_current_date_time() - timedelta(days=1)
        test_date = current_date_time.strftime('%Y-%m-%d')
        test_time = '14:00'

        # when
        response = self.client.post('/book/', data={'first_name': test_name,
                                                    'reservation_date': test_date,
                                                    'reservation_slot': test_time})

        # then
        self.assertContains(response, json.dumps({"message":
                                                  "Booking Failed: Date/Time is in the past.",
                                                  "reservations": []}),
                                                      status_code=200)

    def test_handler404_success(self):
        """HR Test case test_handler404_success
        Parameters
        ----------
        self : TestCase
        """
        # when
        response = self.client.get('/reservations/invalid')

        # then
        self.assertContains(response, '<h1>Page Not Found: /reservations/invalid</h1>\n    ' +
                            '</div>\n<body>', 
                            status_code=404 )
        self.assertTemplateUsed(response, 'error.html')

    def test_version_success(self):
        """HR Test case test_version_success
        Parameters
        ----------
        self : TestCase
        """
        # given
        request = self.factory.get('/version')

        # when
        response = Views.version(request)

        # then
        app_version = response.content.decode()
        # status code check
        self.assertEqual(response.status_code, 200)
        # assert if pattern match is true
        version_regex = r'\d\.\d\.\d'
        pattern = re.compile(version_regex)
        match = bool(pattern.match(app_version))
        self.assertTrue(match)
        # assert regular expression pattern match directly with django.test
        self.assertRegex(app_version, version_regex)

    def test_version_success_with_examples(self):
        """HR Test case test_version_success_with_examples
        Parameters
        ----------
        self : TestCase
        """
        # when
        response = self.client.get('/version/')

        # then
        pattern = re.compile(r'\d\.\d\.\d')
        # assert actual
        match = bool(pattern.match(response.content.decode()))
        self.assertTrue(match)
        # assert sample values
        self.assertTrue(bool(pattern.match('2.2.1')))
        self.assertFalse(bool(pattern.match('v22.0.0')))
        self.assertTrue(bool(pattern.match('2.2.11')))
        self.assertFalse(bool(pattern.match('a.b.c')))

    def test_get_edit_reservation_form(self):
        """HR Test case test_get_edit_reservation_form
        Parameters
        ----------
        self : TestCase
        """
        request = self.factory.get(
            reverse("edit_reservation", args=[self.reservation.id])
        )
        response = Views.edit_reservation(request, self.reservation.id)
        assert response.status_code == 200
        assert b"Edit Reservation" in response.content or b"form" in response.content

    def test_edit_reservation_success(self):
        """HR Test case test_edit_reservation_success
        Parameters
        ----------
        self : TestCase
        """
        # Change reservation time/date to a new, available slot
        new_date = date.today() + timedelta(days=2)
        new_time = time(11, 0)
        data = {
            "reservation_date": new_date,
            "reservation_slot": new_time.strftime("%H:%M"),
        }
        request = self.factory.post(
            reverse("edit_reservation", args=[self.reservation.id]), data
        )
        response = Views.edit_reservation(request, self.reservation.id)
        # Should redirect on success
        assert response.status_code == 302
        self.reservation.refresh_from_db()
        assert self.reservation.reservation_date == new_date
        assert self.reservation.reservation_slot.hour == new_time.hour

    def test_edit_reservation_conflict(self):
        """HR Test case test_edit_reservation_conflict
        Parameters
        ----------
        self : TestCase
        """
        # Create a conflicting reservation
        conflict = Reservation.objects.create(
            first_name="Bob",
            reservation_date=date.today() + timedelta(days=3),
            reservation_slot=time(12, 0)
        )
        data = {
            "reservation_date": conflict.reservation_date,
            "reservation_slot": conflict.reservation_slot.strftime("%H:%M"),
        }
        request = self.factory.post(
            reverse("edit_reservation", args=[self.reservation.id]), data
        )
        response = Views.edit_reservation(request, self.reservation.id)
        assert response.status_code == 200
        assert b"Booking Failed: Already Reserved." in response.content

    def test_edit_reservation_invalid_form(self):
        """HR Test case test_edit_reservation_invalid_form
        Parameters
        ----------
        self : TestCase
        """
        # Send invalid data (missing reservation_date)
        data = {
            "reservation_slot": "13:00",
        }
        request = self.factory.post(
            reverse("edit_reservation", args=[self.reservation.id]), data
        )
        response = Views.edit_reservation(request, self.reservation.id)
        assert response.status_code == 200
        assert b"form" in response.content
        # Form should show errors
        assert b"This field is required" in response.content or b"required" in response.content

    def test_edit_reservation_not_found(self):
        """HR Test case test_edit_reservation_not_found
        Parameters
        ----------
        self : TestCase
        """
        request = self.factory.get(reverse("edit_reservation", args=[9999]))
        with pytest.raises(Exception):
            Views.edit_reservation(request, 9999)
