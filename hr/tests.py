"""
HR Tests Suite
"""
from datetime import datetime, timedelta
import json
import re
from django.test import TestCase, RequestFactory
from django.core.exceptions import ValidationError
from .models import Reservation
from .forms import ReservationForm
from .time_utils import TimeUtils
from .views import Views

# HR Tests
class HrTests(TestCase):
    """HR Test cases
    """
    def setUp(self):
        self.factory = RequestFactory()

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
        booking_slot = '01:01:01'
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
        self.assertContains(response, '<h3>All Active Reservations</h3>\n        ' +
                            '<table>\n            <tr> \n' +
                            '                <th>#</th>\n' +
                            '                <th>Name</th>\n' +
                            '                <th>Booking Date</th>\n' +
                            '                <th>Booking time</th>\n' +
                            '            </tr>\n            \n' +
                            '        </table>\n        <br />\n        <button type="button" ' +
                            'class="btn btn-primary" onClick="refresh()">Refresh</button>\n    ' +
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
        test_time = current_date_time.strftime('%H:%M')

        # when
        response = self.client.post('/book/', data={'first_name': test_name,
                                                    'reservation_date': test_date,
                                                    'reservation_slot': test_time})

        # then
        self.assertContains(response, json.dumps({"message":
                                                  "Booking Complete: Confirmed for " +
                                                  f"{test_date} at {test_time}:00",
                                                  "reservations": [{
                                                      "id": 1,
                                                      "first_name": test_name,
                                                      "reservation_date": test_date,
                                                      "reservation_slot": test_time + ':00'}]}),
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
        test_time = current_date_time.strftime('%H:%M')

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
