from datetime import date
from typing import Any, List


class HolidaysModel:
    def to_dict(self, holidays: List[tuple[date, str]] | None) -> list[dict[str, str | Any]]:
        holidays_list = []
        for holiday in holidays:
            holidays_dict = {"date": str(holiday[0]), "holiday": holiday[1]}
            holidays_list.append(holidays_dict)
        return holidays_list
