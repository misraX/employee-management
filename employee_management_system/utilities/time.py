from datetime import datetime, timedelta, timezone


class TimeUtility:
    @staticmethod
    def get_current_time():
        return datetime.now(tz=timezone.utc)

    @staticmethod
    def convert_to_timezone(dt: datetime, tz_offset: int) -> datetime:
        """
        Converts a datetime object to a timezone-aware datetime object.


        :param dt: datetime object
        :param tz_offset: int
        :return: datetime object
        """
        return dt.replace(tzinfo=timezone.utc) + timedelta(hours=tz_offset)
