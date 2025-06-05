import pytest
from django.test import TestCase
from datetime import date, timedelta, time
from hr.forms import EditReservationForm, ReservationForm

@pytest.mark.django_db
class TestEditReservationForm(TestCase):
    def test_valid_data(self):
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
        form = EditReservationForm({})
        assert not form.is_valid()
        assert "reservation_date" in form.errors
        assert "reservation_slot" in form.errors

    def test_invalid_date_format(self):
        data = {
            "reservation_date": "not-a-date",
            "reservation_slot": "10:30",
        }
        form = EditReservationForm(data)
        assert not form.is_valid()
        assert "reservation_date" in form.errors

    def test_invalid_time_format(self):
        data = {
            "reservation_date": (date.today() + timedelta(days=1)).isoformat(),
            "reservation_slot": "not-a-time",
        }
        form = EditReservationForm(data)
        assert not form.is_valid()
        assert "reservation_slot" in form.errors

@pytest.mark.django_db
class TestReservationForm:
    def test_valid_data(self):
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
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        form = ReservationForm({
            "first_name": "Al",
            "reservation_date": tomorrow,
            "reservation_slot": ReservationForm.TIME_SLOTS[0][0],
        })
        assert not form.is_valid()
        assert "first_name" in form.errors

    def test_missing_fields(self):
        form = ReservationForm({})
        assert not form.is_valid()
        assert "first_name" in form.errors
        assert "reservation_date" in form.errors
        assert "reservation_slot" in form.errors

    def test_invalid_time_slot_choice(self):
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        form = ReservationForm({
            "first_name": "Alice",
            "reservation_date": tomorrow,
            "reservation_slot": "23:59",  # not in TIME_SLOTS
        })
        assert not form.is_valid()
        assert "reservation_slot" in form.errors
