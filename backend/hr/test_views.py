import json
import re
from datetime import date, timedelta
import pytest
from django.test import RequestFactory, TestCase
from hr.models import Reservation
from hr.views import Views

@pytest.mark.django_db
class ViewsApiTests(TestCase):
    """HR Tests ViewsApiTests
    Parameters
    ----------
    TestCase : Inherits TestCase functions
    """

    def setUp(self):
        """HR Tests setUp"""
        self.factory = RequestFactory()
        self.reservation = Reservation.objects.create(
            first_name="Taylor",
            reservation_date=date.today() + timedelta(days=1),
            reservation_slot="12:00:00"
        )

    def testVersionSuccess(self):
        """HR Test case testVersionSuccess"""
        request = self.factory.get('/version')
        response = Views.version(request)
        app_version = response.content.decode()
        self.assertEqual(response.status_code, 200)
        version_regex = r'\d\.\d\.\d'
        pattern = re.compile(version_regex)
        match = bool(pattern.match(app_version))
        self.assertTrue(match)
        self.assertRegex(app_version, version_regex)

    def testBookingsByIdGetSuccess(self):
        """HR Test case testBookingsByIdGetSuccess"""
        request = self.factory.get(f"/api/reservations/{self.reservation.id}/")
        response = Views.bookingsById(request, self.reservation.id)
        assert response.status_code == 200
        data = json.loads(response.content.decode())
        assert data["first_name"] == "Taylor"
        assert data["id"] == self.reservation.id

    def testBookingsByIdGet404(self):
        """HR Test case testBookingsByIdGet404"""
        request = self.factory.get("/api/reservations/9999/")
        with pytest.raises(Exception):
            Views.bookingsById(request, 9999)

    def testBookingsByIdPutSuccess(self):
        """HR Test case testBookingsByIdPutSuccess"""
        payload = {
            "first_name": "Bob",
            "reservation_date": str(self.reservation.reservation_date),
            "reservation_slot": "01:30 PM"
        }
        request = self.factory.put(
            f"/api/reservations/{self.reservation.id}/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        response = Views.bookingsById(request, self.reservation.id)
        assert response.status_code == 200
        data = json.loads(response.content.decode())
        assert data["first_name"] == "Bob"
        assert data["reservation_slot"] == "01:30 PM"
        assert data["success"] is True

    def testBookingsByIdPutMissingFields(self):
        """HR Test case testBookingsByIdPutMissingFields"""
        payload = {
            "reservation_date": str(self.reservation.reservation_date),
            "reservation_slot": "01:30 PM"
        }
        request = self.factory.put(
            f"/api/reservations/{self.reservation.id}/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        response = Views.bookingsById(request, self.reservation.id)
        assert response.status_code == 400
        data = json.loads(response.content.decode())
        assert "All fields are required." in data["error"]

    def testBookingsByIdPutInvalidTimeFormat(self):
        """HR Test case testBookingsByIdPutInvalidTimeFormat"""
        payload = {
            "first_name": "Charlie",
            "reservation_date": str(self.reservation.reservation_date),
            "reservation_slot": "25:61"  # Invalid time
        }
        request = self.factory.put(
            f"/api/reservations/{self.reservation.id}/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        response = Views.bookingsById(request, self.reservation.id)
        assert response.status_code == 400
        data = json.loads(response.content.decode())
        assert "Invalid time format" in data["error"]

    def testBookingsByIdPutConflict(self):
        """HR Test case testBookingsByIdPutConflict"""
        Reservation.objects.create(
            first_name="Eve",
            reservation_date=self.reservation.reservation_date,
            reservation_slot="14:00:00"
        )
        payload = {
            "first_name": "Taylor",
            "reservation_date": str(self.reservation.reservation_date),
            "reservation_slot": "02:00 PM"  # Same as Eve's, should conflict
        }
        request = self.factory.put(
            f"/api/reservations/{self.reservation.id}/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        response = Views.bookingsById(request, self.reservation.id)
        assert response.status_code == 400
        data = json.loads(response.content.decode())
        assert "Already Reserved" in data["error"]

    def testBookingsByIdMethodNotAllowed(self):
        """HR Test case testBookingsByIdMethodNotAllowed"""
        request = self.factory.delete(f"/api/reservations/{self.reservation.id}/")
        response = Views.bookingsById(request, self.reservation.id)
        assert response.status_code == 405
        data = json.loads(response.content.decode())
        assert "Method not allowed" in data["error"]

    def testBookingsByIdInvalidJson(self):
        """HR Test case testBookingsByIdInvalidJson"""
        request = self.factory.put(
            f"/api/reservations/{self.reservation.id}/",
            data="not a json",
            content_type="application/json"
        )
        response = Views.bookingsById(request, self.reservation.id)
        assert response.status_code == 400
        assert "Invalid JSON body" in json.loads(response.content.decode())["error"]

    def testSaveReservationSuccess(self):
        """HR Test case testSaveReservationSuccess"""
        payload = {
            "first_name": "TestGuy",
            "reservation_date": str(date.today() + timedelta(days=3)),
            "reservation_slot": "02:30 PM"
        }
        request = self.factory.put(
            "/api/save_reservation/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        response = Views.saveReservation(request)
        assert response.status_code == 201
        data = json.loads(response.content.decode())
        assert data["first_name"] == "TestGuy"
        assert data["success"] is True

    def testSaveReservationDuplicate(self):
        """HR Test case testSaveReservationDuplicate"""
        slot_time = "03:00 PM"
        res_date = str(date.today() + timedelta(days=2))
        Reservation.objects.create(
            first_name="Dup",
            reservation_date=res_date,
            reservation_slot="15:00:00"
        )
        payload = {
            "first_name": "Another",
            "reservation_date": res_date,
            "reservation_slot": slot_time
        }
        request = self.factory.put(
            "/api/save_reservation/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        response = Views.saveReservation(request)
        assert response.status_code == 400
        data = json.loads(response.content.decode())
        assert "Already Reserved" in data["error"]

    def testSaveReservationBadMethod(self):
        """HR Test case testSaveReservationBadMethod"""
        request = self.factory.get("/api/save_reservation/")
        response = Views.saveReservation(request)
        assert response.status_code == 405
        assert "Method not allowed" in json.loads(response.content.decode())["error"]

    def testSaveReservationInvalidJson(self):
        """HR Test case testSaveReservationInvalidJson"""
        request = self.factory.put(
            "/api/save_reservation/",
            data="bad json",
            content_type="application/json"
        )
        response = Views.saveReservation(request)
        assert response.status_code == 400
        assert "Invalid JSON body" in json.loads(response.content.decode())["error"]

    def testSaveReservationMissingFields(self):
        """HR Test case testSaveReservationMissingFields"""
        payload = {
            "first_name": "MissingFields"
            # missing date and slot
        }
        request = self.factory.put(
            "/api/save_reservation/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        response = Views.saveReservation(request)
        assert response.status_code == 400
        assert "All fields are required" in json.loads(response.content.decode())["error"]

    def testSaveReservationInvalidTime(self):
        """HR Test case testSaveReservationInvalidTime"""
        payload = {
            "first_name": "Test",
            "reservation_date": str(date.today() + timedelta(days=1)),
            "reservation_slot": "notatime"
        }
        request = self.factory.put(
            "/api/save_reservation/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        response = Views.saveReservation(request)
        assert response.status_code == 400
        assert "reservation_slot must be in format" in json.loads(response.content.decode())["error"]
