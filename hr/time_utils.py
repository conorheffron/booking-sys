"""time_utils date_time helper methods
"""
from datetime import date, time, datetime, timedelta
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
        slots = []
        current_time = start_time
        while current_time < end_time:
            slots.append((current_time.strftime("%H:%M"), current_time.strftime("%H:%M")))
            current_time = (datetime.combine(date.today(), current_time) + timedelta(minutes=interval_minutes)).time()
        return slots
    

    @classmethod
    def convertStrToTimeFormat(cls, time_str):
        return datetime.strptime(time_str, "%H:%M").time()
