from datetime import date
from typing import List


class HolidaysModel:
    def to_dict(self, holidays: List[tuple[date, str]] | None):
        holidays_dict = {}
        for holiday in holidays:
            holidays_dict["date"] = str(holiday[0])
            holidays_dict["holiday"] = holiday[1]
        return holidays_dict
