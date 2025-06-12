"""HR Tests Suite"""
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

    def test_version_success(self):
        """HR Test case test_version_success"""
        request = self.factory.get('/version')
        response = Views.version(request)
        app_version = response.content.decode()
        self.assertEqual(response.status_code, 200)
        version_regex = r'\d\.\d\.\d'
        pattern = re.compile(version_regex)
        match = bool(pattern.match(app_version))
        self.assertTrue(match)
        self.assertRegex(app_version, version_regex)

    def test_bookings_by_id_get_success(self):
        """HR Test case test_bookings_by_id_get_success"""
        request = self.factory.get(f"/api/reservations/{self.reservation.id}/")
        response = Views.bookings_by_id(request, self.reservation.id)
        assert response.status_code == 200
        data = json.loads(response.content.decode())
        assert data["first_name"] == "Taylor"
        assert data["id"] == self.reservation.id

    def test_bookings_by_id_get_404(self):
        """HR Test case test_bookings_by_id_get_404"""
        request = self.factory.get("/api/reservations/9999/")
        with pytest.raises(Exception):
            Views.bookings_by_id(request, 9999)

    def test_bookings_by_id_put_success(self):
        """HR Test case test_bookings_by_id_put_success"""
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
        response = Views.bookings_by_id(request, self.reservation.id)
        assert response.status_code == 200
        data = json.loads(response.content.decode())
        assert data["first_name"] == "Bob"
        assert data["reservation_slot"] == "01:30 PM"
        assert data["success"] is True

    def test_bookings_by_id_put_missing_fields(self):
        """HR Test case test_bookings_by_id_put_missing_fields"""
        payload = {
            "reservation_date": str(self.reservation.reservation_date),
            "reservation_slot": "01:30 PM"
        }
        request = self.factory.put(
            f"/api/reservations/{self.reservation.id}/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        response = Views.bookings_by_id(request, self.reservation.id)
        assert response.status_code == 400
        data = json.loads(response.content.decode())
        assert "All fields are required." in data["error"]

    def test_bookings_by_id_put_invalid_time_format(self):
        """HR Test case test_bookings_by_id_put_invalid_time_format"""
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
        response = Views.bookings_by_id(request, self.reservation.id)
        assert response.status_code == 400
        data = json.loads(response.content.decode())
        assert "Invalid time format" in data["error"]

    def test_bookings_by_id_put_conflict(self):
        """HR Test case test_bookings_by_id_put_conflict"""
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
        response = Views.bookings_by_id(request, self.reservation.id)
        assert response.status_code == 400
        data = json.loads(response.content.decode())
        assert "Already Reserved" in data["error"]

    def test_bookings_by_id_method_not_allowed(self):
        """HR Test case test_bookings_by_id_method_not_allowed"""
        request = self.factory.delete(f"/api/reservations/{self.reservation.id}/")
        response = Views.bookings_by_id(request, self.reservation.id)
        assert response.status_code == 405
        data = json.loads(response.content.decode())
        assert "Method not allowed" in data["error"]

    def test_bookings_by_id_invalid_json(self):
        """HR Test case test_bookings_by_id_invalid_json"""
        request = self.factory.put(
            f"/api/reservations/{self.reservation.id}/",
            data="not a json",
            content_type="application/json"
        )
        response = Views.bookings_by_id(request, self.reservation.id)
        assert response.status_code == 400
        assert "Invalid JSON body" in json.loads(response.content.decode())["error"]

    def test_save_reservation_success(self):
        """HR Test case test_save_reservation_success"""
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
        response = Views.save_reservation(request)
        assert response.status_code == 201
        data = json.loads(response.content.decode())
        assert data["first_name"] == "TestGuy"
        assert data["success"] is True

    def test_save_reservation_duplicate(self):
        """HR Test case test_save_reservation_duplicate"""
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
        response = Views.save_reservation(request)
        assert response.status_code == 400
        data = json.loads(response.content.decode())
        assert "Already Reserved" in data["error"]

    def test_save_reservation_bad_method(self):
        """HR Test case test_save_reservation_bad_method"""
        request = self.factory.get("/api/save_reservation/")
        response = Views.save_reservation(request)
        assert response.status_code == 405
        assert "Method not allowed" in json.loads(response.content.decode())["error"]

    def test_save_reservation_invalid_json(self):
        """HR Test case test_save_reservation_invalid_json"""
        request = self.factory.put(
            "/api/save_reservation/",
            data="bad json",
            content_type="application/json"
        )
        response = Views.save_reservation(request)
        assert response.status_code == 400
        assert "Invalid JSON body" in json.loads(response.content.decode())["error"]

    def test_save_reservation_missing_fields(self):
        """HR Test case test_save_reservation_missing_fields"""
        payload = {
            "first_name": "MissingFields"
            # missing date and slot
        }
        request = self.factory.put(
            "/api/save_reservation/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        response = Views.save_reservation(request)
        assert response.status_code == 400
        assert "All fields are required" in json.loads(response.content.decode())["error"]

    def test_save_reservation_invalid_time(self):
        """HR Test case test_save_reservation_invalid_time"""
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
        response = Views.save_reservation(request)
        assert response.status_code == 400
        assert "reservation_slot must be in format" in json.loads(
            response.content.decode())["error"]
