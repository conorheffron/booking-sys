from datetime import datetime
import pytz

class TimeUtils:

    @classmethod
    def get_current_date_time(self):
        tz = pytz.timezone('UTC')
        tz_time = tz.localize(datetime.now())
        london_tz = pytz.timezone('Europe/London')
        return tz_time.astimezone(london_tz)
