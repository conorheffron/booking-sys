"""HR Tests Suite"""
import json
import re
from datetime import date, timedelta
from unittest.mock import patch, Mock
import pytest
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.models import User
from hr.models import Reservation
from hr.views import Views, csrf_view, version_view, table_view, bookings_by_id_view, save_reservation_view

@pytest.mark.django_db
class ApiTests(TestCase):
    """HR Tests ApiTests
    Parameters
    ----------
    TestCase : Inherits TestCase functions
    """

    def setUp(self):
        """HR Tests setUp"""
        self.views = Views()
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username="apiuser",
            email="api@example.com",
            password="testpassword"
        )
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
        response = self.views.bookings_by_id(request, self.reservation.id)
        assert response.status_code == 200
        data = json.loads(response.content.decode())
        assert data["first_name"] == "Taylor"
        assert data["id"] == self.reservation.id

    def test_bookings_by_id_get_404(self):
        """HR Test case test_bookings_by_id_get_404"""
        request = self.factory.get("/api/reservations/9999/")
        with pytest.raises(Exception):
            self.views.bookings_by_id(request, 9999)

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
        request.user = self.user
        response = self.views.bookings_by_id(request, self.reservation.id)
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
        request.user = self.user
        response = self.views.bookings_by_id(request, self.reservation.id)
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
        request.user = self.user
        response = self.views.bookings_by_id(request, self.reservation.id)
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
        request.user = self.user
        response = self.views.bookings_by_id(request, self.reservation.id)
        assert response.status_code == 400
        data = json.loads(response.content.decode())
        assert "Already Reserved" in data["error"]

    def test_bookings_by_id_delete_success(self):
        """HR Test case test_bookings_by_id_delete_success"""
        # Ensure the reservation exists
        assert Reservation.objects.filter(id=self.reservation.id).exists()
        request = self.factory.delete(f"/api/reservations/{self.reservation.id}/")
        request.user = self.user
        response = self.views.bookings_by_id(request, self.reservation.id)
        assert response.status_code == 200
        data = json.loads(response.content.decode())
        assert data["success"] is True
        assert "deleted" in data["message"].lower()
        # Confirm it's deleted from the database
        assert not Reservation.objects.filter(id=self.reservation.id).exists()

    def test_bookings_by_id_delete_404(self):
        """HR Test case test_bookings_by_id_delete_404"""
        # Attempt to delete a reservation that does not exist
        request = self.factory.delete("/api/reservations/9999/")
        with pytest.raises(Exception):
            self.views.bookings_by_id(request, 9999)

    def test_bookings_by_id_method_not_allowed(self):
        """HR Test case test_bookings_by_id_method_not_allowed"""
        # PATCH is not allowed
        request = self.factory.patch(f"/api/reservations/{self.reservation.id}/")
        response = self.views.bookings_by_id(request, self.reservation.id)
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
        request.user = self.user
        response = self.views.bookings_by_id(request, self.reservation.id)
        assert response.status_code == 400
        assert "Invalid JSON body" in json.loads(response.content.decode())["error"]

    def test_bookings_by_id_put_requires_auth(self):
        """HR Test case test_bookings_by_id_put_requires_auth"""
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
        request.user = AnonymousUser()
        response = self.views.bookings_by_id(request, self.reservation.id)
        assert response.status_code == 401
        assert "Authentication required" in json.loads(response.content.decode())["error"]

    def test_bookings_by_id_delete_requires_auth(self):
        """HR Test case test_bookings_by_id_delete_requires_auth"""
        request = self.factory.delete(f"/api/reservations/{self.reservation.id}/")
        request.user = AnonymousUser()
        response = self.views.bookings_by_id(request, self.reservation.id)
        assert response.status_code == 401
        assert "Authentication required" in json.loads(response.content.decode())["error"]

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
        response = self.views.save_reservation(request)
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
        response = self.views.save_reservation(request)
        assert response.status_code == 400
        data = json.loads(response.content.decode())
        assert "Already Reserved" in data["error"]

    def test_save_reservation_bad_method(self):
        """HR Test case test_save_reservation_bad_method"""
        request = self.factory.get("/api/save_reservation/")
        response = self.views.save_reservation(request)
        assert response.status_code == 405
        assert "Method not allowed" in json.loads(response.content.decode())["error"]

    def test_save_reservation_invalid_json(self):
        """HR Test case test_save_reservation_invalid_json"""
        request = self.factory.put(
            "/api/save_reservation/",
            data="bad json",
            content_type="application/json"
        )
        response = self.views.save_reservation(request)
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
        response = self.views.save_reservation(request)
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
        response = self.views.save_reservation(request)
        assert response.status_code == 400
        assert "reservation_slot must be in format" in json.loads(
            response.content.decode())["error"]

    def test_csrf_success(self):
        """HR Test case test_csrf_success"""
        request = self.factory.get('/api/csrf/')
        request.META["CSRF_COOKIE"] = "token-123"
        response = Views.csrf(request)
        assert response.status_code == 200
        assert json.loads(response.content.decode())["csrfToken"] == "token-123"

    def test_table_view_with_query_date(self):
        """HR Test case test_table_view_with_query_date"""
        target_date = str(date.today() + timedelta(days=2))
        Reservation.objects.create(
            first_name="Future",
            reservation_date=target_date,
            reservation_slot="11:00:00"
        )
        request = self.factory.get(f'/api/bookings?date={target_date}')
        response = Views.table_view(request)
        data = json.loads(response.content.decode())
        assert response.status_code == 200
        assert data["message"] == "success"
        assert len(data["reservations"]) == 1
        assert data["reservations"][0]["first_name"] == "Future"

    def test_table_view_without_query_date_returns_future(self):
        """HR Test case test_table_view_without_query_date_returns_future"""
        Reservation.objects.create(
            first_name="Past",
            reservation_date=str(date.today() - timedelta(days=1)),
            reservation_slot="09:00:00"
        )
        Reservation.objects.create(
            first_name="Future",
            reservation_date=str(date.today() + timedelta(days=3)),
            reservation_slot="10:00:00"
        )
        request = self.factory.get('/api/bookings')
        response = Views.table_view(request)
        data = json.loads(response.content.decode())
        assert response.status_code == 200
        assert len(data["reservations"]) == 2  # includes self.reservation from setUp
        first_names = [booking["first_name"] for booking in data["reservations"]]
        assert "Future" in first_names
        assert "Past" not in first_names

    def test_bookings_by_id_put_invalid_reservation_date(self):
        """HR Test case test_bookings_by_id_put_invalid_reservation_date"""
        payload = {
            "first_name": "Taylor",
            "reservation_date": "invalid-date",
            "reservation_slot": "02:00 PM"
        }
        request = self.factory.put(
            f"/api/reservations/{self.reservation.id}/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        request.user = self.user
        response = self.views.bookings_by_id(request, self.reservation.id)
        assert response.status_code == 400
        assert "Invalid reservation_date or reservation_slot." in json.loads(
            response.content.decode()
        )["error"]

    def test_bookings_by_id_put_past_date_time_rejected(self):
        """HR Test case test_bookings_by_id_put_past_date_time_rejected"""
        payload = {
            "first_name": "Taylor",
            "reservation_date": str(date.today() - timedelta(days=1)),
            "reservation_slot": "10:00 AM"
        }
        request = self.factory.put(
            f"/api/reservations/{self.reservation.id}/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        request.user = self.user
        response = self.views.bookings_by_id(request, self.reservation.id)
        assert response.status_code == 400
        assert "Cannot update reservation to a past date/time." in json.loads(
            response.content.decode()
        )["error"]

    def test_save_reservation_invalid_date_rejected(self):
        """HR Test case test_save_reservation_invalid_date_rejected"""
        payload = {
            "first_name": "Test",
            "reservation_date": "not-a-date",
            "reservation_slot": "10:00 AM"
        }
        request = self.factory.put(
            "/api/save_reservation/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        response = self.views.save_reservation(request)
        assert response.status_code == 400
        assert "Invalid reservation_date or reservation_slot." in json.loads(
            response.content.decode()
        )["error"]

    def test_save_reservation_past_date_rejected(self):
        """HR Test case test_save_reservation_past_date_rejected"""
        payload = {
            "first_name": "Test",
            "reservation_date": str(date.today() - timedelta(days=1)),
            "reservation_slot": "10:00 AM"
        }
        request = self.factory.put(
            "/api/save_reservation/",
            data=json.dumps(payload),
            content_type="application/json"
        )
        response = self.views.save_reservation(request)
        assert response.status_code == 400
        assert "Cannot make a reservation for a past date/time." in json.loads(
            response.content.decode()
        )["error"]

    @patch("hr.views.render")
    def test_edit_reservation_get_initial_form(self, mock_render):
        """HR Test case test_edit_reservation_get_initial_form"""
        mock_render.return_value = HttpResponse("ok")
        request = self.factory.get(f"/api/reservations/edit/{self.reservation.id}/")
        response = Views.edit_reservation(request, self.reservation.id)
        assert response.status_code == 200
        args, _ = mock_render.call_args
        assert args[1] == "edit_reservation.html"
        assert args[2]["reservation"].id == self.reservation.id
        assert args[2]["form"].initial["reservation_date"] == self.reservation.reservation_date

    @patch("hr.views.render")
    def test_edit_reservation_blocks_past_booking(self, mock_render):
        """HR Test case test_edit_reservation_blocks_past_booking"""
        mock_render.return_value = HttpResponse("blocked")
        past_reservation = Reservation.objects.create(
            first_name="Old",
            reservation_date=date.today() - timedelta(days=1),
            reservation_slot="09:00:00"
        )
        request = self.factory.get(f"/api/reservations/edit/{past_reservation.id}/")
        response = Views.edit_reservation(request, past_reservation.id)
        assert response.status_code == 200
        args, _ = mock_render.call_args
        assert args[2]["form"] is None
        assert "Editing past bookings is not allowed." in args[2]["error"]

    @patch("hr.views.render")
    def test_edit_reservation_post_conflict(self, mock_render):
        """HR Test case test_edit_reservation_post_conflict"""
        mock_render.return_value = HttpResponse("conflict")
        future_date = date.today() + timedelta(days=2)
        Reservation.objects.create(
            first_name="Clash",
            reservation_date=future_date,
            reservation_slot="11:00:00"
        )
        request = self.factory.post(
            f"/api/reservations/edit/{self.reservation.id}/",
            data={"reservation_date": str(future_date), "reservation_slot": "11:00"}
        )
        response = Views.edit_reservation(request, self.reservation.id)
        assert response.status_code == 200
        args, _ = mock_render.call_args
        assert "Already Reserved" in args[2]["error"]

    @patch("hr.views.render")
    def test_edit_reservation_post_past_datetime(self, mock_render):
        """HR Test case test_edit_reservation_post_past_datetime"""
        mock_render.return_value = HttpResponse("past")
        request = self.factory.post(
            f"/api/reservations/edit/{self.reservation.id}/",
            data={
                "reservation_date": str(date.today() - timedelta(days=1)),
                "reservation_slot": "09:00"
            }
        )
        response = Views.edit_reservation(request, self.reservation.id)
        assert response.status_code == 200
        args, _ = mock_render.call_args
        assert "past date/time" in args[2]["error"]

    @patch("hr.views.redirect")
    def test_edit_reservation_post_success_redirect(self, mock_redirect):
        """HR Test case test_edit_reservation_post_success_redirect"""
        mock_redirect.return_value = HttpResponse("redirected")
        future_date = date.today() + timedelta(days=4)
        request = self.factory.post(
            f"/api/reservations/edit/{self.reservation.id}/",
            data={"reservation_date": str(future_date), "reservation_slot": "12:30"}
        )
        response = Views.edit_reservation(request, self.reservation.id)
        self.reservation.refresh_from_db()
        assert response.status_code == 200
        assert mock_redirect.call_args[0][0] == "reservations"
        assert self.reservation.reservation_date == future_date

    def test_wrapper_views(self):
        """HR Test case test_wrapper_views"""
        csrf_request = self.factory.get('/api/csrf/')
        csrf_request.META["CSRF_COOKIE"] = "wrapper-token"
        csrf_response = csrf_view(csrf_request)
        assert csrf_response.status_code == 200

        version_response = version_view(self.factory.get('/api/version/'))
        assert version_response.status_code == 200

        table_response = table_view(self.factory.get('/api/bookings?date=bad-date'))
        assert table_response.status_code == 200

        bookings_response = bookings_by_id_view(
            self.factory.get(f"/api/bookingsById/{self.reservation.id}"),
            self.reservation.id
        )
        assert bookings_response.status_code == 200

        save_response = save_reservation_view(self.factory.get("/api/reservations"))
        assert save_response.status_code == 405

    def test_auth_status_success(self):
        """HR Test case test_auth_status_success"""
        request = self.factory.get("/api/auth/status")
        request.user = AnonymousUser()
        response = Views.auth_status(request)
        assert response.status_code == 200
        data = json.loads(response.content.decode())
        assert data["authenticated"] is False
        assert data["username"] is None

    def test_login_invalid_credentials(self):
        """HR Test case test_login_invalid_credentials"""
        login_request = self.factory.post(
            "/api/auth/login/",
            data=json.dumps({"username": "apiuser", "password": "wrong-password"}),
            content_type="application/json"
        )
        login_response = Views.login(login_request)
        assert login_response.status_code == 401
        login_data = json.loads(login_response.content.decode())
        assert "Invalid credentials" in login_data["error"]

    def test_logout_success(self):
        """HR Test case test_logout_success"""
        logout_request = self.factory.post("/api/auth/logout/")
        logout_request.session = Mock()
        logout_request.user = self.user
        logout_response = Views.logout(logout_request)
        assert logout_response.status_code == 200
        logout_data = json.loads(logout_response.content.decode())
        assert logout_data["success"] is True
