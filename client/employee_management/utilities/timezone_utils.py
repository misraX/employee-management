from datetime import datetime

import pytz


class TimezoneUtils:
    """
    A mocked timezone utility class, acts as a client local time,
    and defaulted to 'America/New_York' timezone.
    """

    def __init__(self, timezone: str = "America/New_York"):
        self.local_tz = pytz.timezone(timezone)

    def to_local_timezone(self, dt_str: str, date_format: str = "%Y-%m-%d %H:%M:%S.%f%z") -> str:
        """Convert a string representation of a datetime object to the local timezone."""
        dt = datetime.strptime(dt_str, date_format)
        local_dt = dt.astimezone(self.local_tz)
        return local_dt.strftime(date_format)
