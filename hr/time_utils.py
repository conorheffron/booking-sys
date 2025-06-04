"""time_utils date_time helper methods
"""
from datetime import date, datetime, timedelta
import pytz

class TimeUtils:
    """TimeUtils is utility class for generating/manipulating datetime
    """

    @classmethod
    def get_current_date_time(cls):
        """Get the current date time value
        Parameters
        ----------
        """
        tz = pytz.timezone('UTC')
        tz_time = tz.localize(datetime.now())
        london_tz = pytz.timezone('Europe/London')
        return tz_time.astimezone(london_tz)

    @classmethod
    def generate_time_slots(cls, start_time, end_time, interval_minutes):
        """Generate list of valid time slots for reservations
        Parameters
        ----------
        start_time: The start time in format %HH:%MM i.e. 09:30
        end_time: The end time in format %HH:%MM i.e. 14:00
        interval_minutes: The gap between time slots i.e. 15/30/45 mins
        """
        slots = []
        current_time = start_time
        while current_time < end_time:
            slots.append((current_time.strftime("%H:%M"), current_time.strftime("%H:%M")))
            time_diff = timedelta(minutes=interval_minutes)
            current_time = (datetime.combine(date.today(), current_time) + time_diff).time()
        return slots

    @classmethod
    def convert_str_to_time(cls, time_str):
        """Converts string value used to represent reservation slot into valid time value
        Parameters
        ----------
        time_str: The time string in format %HH:%MM i.e. '09:30'
        """
        return datetime.strptime(time_str, "%H:%M").time()
