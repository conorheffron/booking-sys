"""
Forms Test Suites
"""
from datetime import date, timedelta
import pytest
from django.test import TestCase
from hr.forms import EditReservationForm, ReservationForm

@pytest.mark.django_db
class TestEditReservationForm(TestCase):
    """
    Test suite for the EditReservationForm.

    This class contains unit tests to validate form behavior for editing a reservation,
    including handling of valid input, missing fields, and invalid data formats.
    """

    def test_valid_data(self):
        """
        Test that the form is valid when provided with correct reservation date and time.
        """
        data = {
            "reservation_date": (date.today() + timedelta(days=1)).isoformat(),
            "reservation_slot": "10:30",
        }
        form = EditReservationForm(data)
        assert form.is_valid()
        assert form.cleaned_data["reservation_date"] == date.today() + timedelta(days=1)
        assert form.cleaned_data["reservation_slot"].hour == 10
        assert form.cleaned_data["reservation_slot"].minute == 30

    def test_missing_required_fields(self):
        """
        Test that the form is invalid when required fields are missing.
        """
        form = EditReservationForm({})
        assert not form.is_valid()
        assert "reservation_date" in form.errors
        assert "reservation_slot" in form.errors

    def test_invalid_date_format(self):
        """
        Test that the form is invalid when the reservation_date is not a valid date.
        """
        data = {
            "reservation_date": "not-a-date",
            "reservation_slot": "10:30",
        }
        form = EditReservationForm(data)
        assert not form.is_valid()
        assert "reservation_date" in form.errors

    def test_invalid_time_format(self):
        """
        Test that the form is invalid when the reservation_slot is not a valid time.
        """
        data = {
            "reservation_date": (date.today() + timedelta(days=1)).isoformat(),
            "reservation_slot": "not-a-time",
        }
        form = EditReservationForm(data)
        assert not form.is_valid()
        assert "reservation_slot" in form.errors

@pytest.mark.django_db
class TestReservationForm(TestCase):
    """
    Test suite for the ReservationForm.

    This class contains unit tests to check the validation logic for creating a new reservation,
    covering valid input, short first names, missing fields, and invalid time slot choices.
    """

    def test_valid_data(self):
        """
        Test that the form is valid when provided with correct name, date, and time slot.
        """
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        # Test using first available slot from TIME_SLOTS
        form = ReservationForm({
            "first_name": "Alice",
            "reservation_date": tomorrow,
            "reservation_slot": ReservationForm.TIME_SLOTS[0][0],  # e.g. "09:00"
        })
        assert form.is_valid()
        assert form.cleaned_data["first_name"] == "Alice"
        assert form.cleaned_data["reservation_date"] == date.fromisoformat(tomorrow)
        assert form.cleaned_data["reservation_slot"] == ReservationForm.TIME_SLOTS[0][0]

    def test_first_name_too_short(self):
        """
        Test that the form is invalid if the first name is shorter than the minimum length.
        """
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        form = ReservationForm({
            "first_name": "Al",
            "reservation_date": tomorrow,
            "reservation_slot": ReservationForm.TIME_SLOTS[0][0],
        })
        assert not form.is_valid()
        assert "first_name" in form.errors

    def test_missing_fields(self):
        """
        Test that the form is invalid when required fields are missing.
        """
        form = ReservationForm({})
        assert not form.is_valid()
        assert "first_name" in form.errors
        assert "reservation_date" in form.errors
        assert "reservation_slot" in form.errors

    def test_invalid_time_slot_choice(self):
        """
        Test that the form is invalid when an unavailable time slot is selected.
        """
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        form = ReservationForm({
            "first_name": "Alice",
            "reservation_date": tomorrow,
            "reservation_slot": "23:59",  # not in TIME_SLOTS
        })
        assert not form.is_valid()
        assert "reservation_slot" in form.errors
