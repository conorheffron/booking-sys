"""time_utils date_time helper methods
"""
from datetime import datetime
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
